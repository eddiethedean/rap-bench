# rap-bench

**Fake Async Detector CLI — expose event loop stalls caused by fake async implementations.**

---

## Why `rap*`?

Packages prefixed with **`rap`** stand for **Real Async Python**. Unlike many libraries that merely wrap blocking I/O in `async` syntax, `rap*` packages guarantee that all I/O work is executed **outside the Python GIL** using native runtimes (primarily Rust). This means event loops are never stalled by hidden thread pools, blocking syscalls, or cooperative yielding tricks. If a `rap*` API is `async`, it is *structurally non-blocking by design*, not by convention. The `rap` prefix is a contract: measurable concurrency, real parallelism, and verifiable async behavior under load.

See the [rap-manifesto](https://github.com/rap-project/rap-manifesto) for philosophy and guarantees.

---

## What this package provides

- Fake Async Detector CLI tool
- Automated benchmarks for async libraries
- Event loop stall detection
- Throughput and latency measurements
- Pass/fail criteria validation

---

## Installation

```bash
pip install rap-bench
```

---

## Usage

```bash
# List available test libraries
rap-bench list

# Run detector on rapfiles
rap-bench detect rapfiles

# Run with custom configuration
rap-bench detect rapfiles --tasks 1000 --blocking-tasks 1

# Test other libraries for comparison
rap-bench detect asyncio-files
```

---

## Benchmarks

The Fake Async Detector:

1. Launches 1 blocking or slow task
2. Launches 100–1000 concurrent I/O tasks
3. Measures:
   - Throughput
   - p50 / p95 latency
   - Event loop stall gaps

**Pass Criteria:**
- No collapse in unrelated task progress
- Stable latency under contention
- Zero event loop stalls

---

## Non-Goals

- Not a general-purpose benchmarking tool
- Not compatible with all async libraries (intentional)
- Not designed for non-async code

---

## License

MIT

