# rap-bench

**Fake Async Detector CLI — expose event loop stalls caused by fake async implementations.**

[![PyPI version](https://badge.fury.io/py/rap-bench.svg)](https://badge.fury.io/py/rap-bench)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`rap-bench` is a CLI tool that exposes event loop stalls caused by fake async implementations. It provides automated benchmarks for async libraries, measuring throughput, latency, and event loop behavior under contention to verify true async performance.

## Why `rap*`?

Packages prefixed with **`rap`** stand for **Real Async Python**. Unlike many libraries that merely wrap blocking I/O in `async` syntax, `rap*` packages guarantee that all I/O work is executed **outside the Python GIL** using native runtimes (primarily Rust). This means event loops are never stalled by hidden thread pools, blocking syscalls, or cooperative yielding tricks. If a `rap*` API is `async`, it is *structurally non-blocking by design*, not by convention. The `rap` prefix is a contract: measurable concurrency, real parallelism, and verifiable async behavior under load.

See the [rap-manifesto](https://github.com/rap-project/rap-manifesto) for philosophy and guarantees.

## Features

- ✅ **Fake Async Detector** CLI tool
- ✅ **Automated benchmarks** for async libraries
- ✅ **Event loop stall** detection
- ✅ **Throughput and latency** measurements
- ✅ **Pass/fail criteria** validation
- ✅ **Multiple test libraries** included

## Requirements

- Python 3.8+

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

## How It Works

The Fake Async Detector:

1. **Launches 1 blocking or slow task** - Simulates a blocking operation
2. **Launches 100–1000 concurrent I/O tasks** - Creates contention
3. **Measures:**
   - Throughput (operations per second)
   - p50 / p95 latency percentiles
   - Event loop stall gaps
   - Task completion rates

**Pass Criteria:**
- ✅ No collapse in unrelated task progress
- ✅ Stable latency under contention
- ✅ Zero event loop stalls

## Example Output

```
Testing rapfiles...
✓ All tasks completed successfully
✓ Throughput: 1250 ops/sec
✓ p50 latency: 2.3ms
✓ p95 latency: 5.1ms
✓ Event loop stalls: 0
✅ PASSED: rapfiles is true async
```

## Supported Libraries

Run `rap-bench list` to see all available test libraries:

- `rapfiles` - True async filesystem I/O
- `rapsqlite` - True async SQLite
- `rapcsv` - Streaming async CSV
- `aiosqlite` - For comparison (known fake async)
- `asyncio-files` - For comparison (known fake async)

## Advanced Usage

```bash
# Custom configuration
rap-bench detect rapfiles --tasks 1000 --blocking-tasks 2

# Verbose output
rap-bench detect rapfiles --verbose

# Save results to file
rap-bench detect rapfiles --output results.json
```

## Related Projects

- [rap-manifesto](https://github.com/rap-project/rap-manifesto) - Philosophy and guarantees
- [rapfiles](https://github.com/rap-project/rapfiles) - True async filesystem I/O
- [rapsqlite](https://github.com/rap-project/rapsqlite) - True async SQLite
- [rapcsv](https://github.com/rap-project/rapcsv) - Streaming async CSV

## Limitations

- Not a general-purpose benchmarking tool
- Not compatible with all async libraries (intentional)
- Not designed for non-async code

## Contributing

Contributions are welcome! Please see our [contributing guidelines](https://github.com/rap-project/rap-bench/blob/main/CONTRIBUTING.md) (coming soon).

## License

MIT

## Changelog

See [CHANGELOG.md](https://github.com/rap-project/rap-bench/blob/main/CHANGELOG.md) (coming soon) for version history.

