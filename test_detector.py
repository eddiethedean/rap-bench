"""Test the detector with rapfiles."""

import asyncio
from rap_bench.detector import detect_fake_async
from rap_bench.libraries import test_rapfiles


async def main():
    """Run detector test."""
    # Test test_rapfiles directly first
    print("Testing test_rapfiles directly...")
    try:
        result = await test_rapfiles()
        print(f"Direct test result: {result}")
    except Exception as e:
        import traceback
        print(f"Direct test error: {e}")
        traceback.print_exc()
    
    # Now test with detector
    print("\nTesting with detector...")
    try:
        result = await detect_fake_async(
            test_rapfiles,
            total_tasks=2,
            blocking_tasks=1,
        )
        print(f"Success: {result.successful_tasks}")
        print(f"Failed: {result.failed_tasks}")
        print(f"Passed: {result.passed}")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

