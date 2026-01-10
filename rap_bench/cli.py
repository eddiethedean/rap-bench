"""CLI entry point for rap-bench."""

import asyncio
import sys
import argparse
from typing import Optional

from rap_bench.detector import detect_fake_async
from rap_bench.libraries import LIBRARY_TESTS


def format_results(results) -> str:
    """Format detector results for display."""
    status = "✓ PASSED" if results.passed else "✗ FAILED"
    output = f"""
Fake Async Detector Results
{'=' * 60}
Status: {status}
{'=' * 60}

Configuration:
  Total I/O tasks: {results.total_tasks}
  Blocking tasks: {results.blocking_tasks}

Execution:
  Successful tasks: {results.successful_tasks}
  Failed tasks: {results.failed_tasks}
  Total time: {results.total_time:.3f}s
  Throughput: {results.throughput:.2f} tasks/sec

Latency:
  p50: {results.p50_latency*1000:.2f}ms
  p95: {results.p95_latency*1000:.2f}ms

Event Loop:
  Stalls detected: {results.event_loop_stalls}
  Max stall duration: {results.max_stall_duration*1000:.2f}ms

Pass Criteria:
  ✓ Max stall < 10ms: {'✓' if results.max_stall_duration < 0.01 else '✗'}
  ✓ Throughput > 100 tasks/sec: {'✓' if results.throughput > 100 else '✗'}
  ✓ p95 latency < 1s: {'✓' if results.p95_latency < 1.0 else '✗'}
"""
    return output


async def detect(library_name: str, tasks: int = 1000, blocking_tasks: int = 1) -> None:
    """Run the Fake Async Detector on a library."""
    print(f"Running Fake Async Detector on {library_name}...")
    print(f"Configuration: {tasks} I/O tasks, {blocking_tasks} blocking task(s)")
    print("This may take a moment...\n")
    
    # Get test function
    if library_name not in LIBRARY_TESTS:
        print(f"Error: Unknown library '{library_name}'")
        print(f"Available libraries: {', '.join(LIBRARY_TESTS.keys())}")
        sys.exit(1)
    
    test_fn = LIBRARY_TESTS[library_name]
    
    try:
        # Run detector
        results = await detect_fake_async(
            task_fn=test_fn,
            total_tasks=tasks,
            blocking_tasks=blocking_tasks,
        )
        
        # Display results
        print(format_results(results))
        
        # Exit with appropriate code
        sys.exit(0 if results.passed else 1)
    
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running detector: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fake Async Detector - detect event loop stalls in async libraries"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    detect_parser = subparsers.add_parser('detect', help='Detect fake async in a library')
    detect_parser.add_argument('library', help='Library name to test')
    detect_parser.add_argument(
        '--tasks', 
        type=int, 
        default=1000,
        help='Number of concurrent I/O tasks (default: 1000)'
    )
    detect_parser.add_argument(
        '--blocking-tasks',
        type=int,
        default=1,
        help='Number of blocking tasks (default: 1)'
    )
    
    list_parser = subparsers.add_parser('list', help='List available test libraries')
    
    args = parser.parse_args()
    
    if args.command == 'detect':
        asyncio.run(detect(args.library, args.tasks, args.blocking_tasks))
    elif args.command == 'list':
        print("Available test libraries:")
        for lib_name in LIBRARY_TESTS.keys():
            print(f"  - {lib_name}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

