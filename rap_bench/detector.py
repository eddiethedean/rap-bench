"""Fake Async Detector implementation."""

import asyncio
import time
from typing import List, Callable, Awaitable, Dict, Any
from dataclasses import dataclass


@dataclass
class DetectorResults:
    """Results from the Fake Async Detector."""
    total_tasks: int
    blocking_tasks: int
    successful_tasks: int
    failed_tasks: int
    total_time: float
    throughput: float  # tasks per second
    p50_latency: float
    p95_latency: float
    event_loop_stalls: int
    max_stall_duration: float
    passed: bool


async def detect_fake_async(
    task_fn: Callable[[], Awaitable[Any]],
    total_tasks: int = 1000,
    blocking_tasks: int = 1,
    blocking_fn: Callable[[], Awaitable[Any]] | None = None,
) -> DetectorResults:
    """
    Detect fake async implementations by measuring event loop behavior.
    
    Args:
        task_fn: Async function to test (should accept no args and return awaitable)
        total_tasks: Number of concurrent I/O tasks to run
        blocking_tasks: Number of blocking tasks to run concurrently
        blocking_fn: Optional blocking task function (default: sleeps for 1 second)
    
    Returns:
        DetectorResults with metrics and pass/fail status
    """
    if blocking_fn is None:
        # Default blocking task: sleeps for 1 second
        async def default_blocking():
            await asyncio.sleep(1.0)
        blocking_fn = default_blocking
    
    # Track event loop stalls
    stall_durations: List[float] = []
    last_check_time = time.perf_counter()
    check_interval = 0.001  # Check every 1ms
    
    async def monitor_event_loop():
        """Monitor event loop for stalls."""
        nonlocal last_check_time
        while True:
            await asyncio.sleep(check_interval)
            current_time = time.perf_counter()
            elapsed = current_time - last_check_time
            if elapsed > check_interval * 1.5:  # Detect stalls > 50% over expected
                stall_durations.append(elapsed - check_interval)
            last_check_time = current_time
    
    # Start event loop monitor
    monitor_task = asyncio.create_task(monitor_event_loop())
    
    # Start blocking tasks
    blocking_task_list = []
    for _ in range(blocking_tasks):
        blocking_task_list.append(asyncio.create_task(blocking_fn()))
    
    # Track task latencies
    task_start_times: Dict[asyncio.Task, float] = {}
    task_latencies: List[float] = []
    successful_tasks = 0
    failed_tasks = 0
    
    async def run_single_task(task_id: int):
        """Run a single I/O task and track its latency."""
        start_time = time.perf_counter()
        try:
            await task_fn()
            end_time = time.perf_counter()
            latency = end_time - start_time
            task_latencies.append(latency)
            successful_tasks += 1
        except Exception:
            failed_tasks += 1
            end_time = time.perf_counter()
            latency = end_time - start_time
            task_latencies.append(latency)
            raise
    
    # Start all I/O tasks concurrently
    start_time = time.perf_counter()
    io_tasks = [asyncio.create_task(run_single_task(i)) for i in range(total_tasks)]
    
    # Wait for all tasks to complete
    task_results = await asyncio.gather(*io_tasks, return_exceptions=True)
    end_time = time.perf_counter()
    
    # Cancel monitor
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass
    
    # Calculate metrics
    total_time = end_time - start_time
    throughput = successful_tasks / total_time if total_time > 0 else 0
    
    # Calculate percentiles
    sorted_latencies = sorted(task_latencies)
    p50_latency = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0.0
    p95_index = int(len(sorted_latencies) * 0.95)
    p95_latency = sorted_latencies[p95_index] if sorted_latencies and p95_index < len(sorted_latencies) else 0.0
    
    max_stall = max(stall_durations) if stall_durations else 0.0
    
    # Count exceptions from results
    exception_count = len([r for r in task_results if isinstance(r, Exception)])
    
    # Pass criteria:
    # 1. No significant event loop stalls (>10ms)
    # 2. Stable throughput (no collapse under contention)
    # 3. Reasonable latency (p95 < 1 second for simple I/O)
    passed = (
        max_stall < 0.01 and  # No stalls > 10ms
        throughput > 100 and  # At least 100 tasks/sec
        p95_latency < 1.0 and  # p95 latency < 1 second
        successful_tasks > total_tasks * 0.95  # At least 95% success rate
    )
    
    return DetectorResults(
        total_tasks=total_tasks,
        blocking_tasks=blocking_tasks,
        successful_tasks=successful_tasks,
        failed_tasks=exception_count,
        total_time=total_time,
        throughput=throughput,
        p50_latency=p50_latency,
        p95_latency=p95_latency,
        event_loop_stalls=len(stall_durations),
        max_stall_duration=max_stall,
        passed=passed,
    )

