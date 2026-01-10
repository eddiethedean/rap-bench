"""Test implementations for different libraries."""

import asyncio
import tempfile
import os
from typing import Callable, Awaitable, Any


async def test_rapfiles():
    """Test rapfiles library."""
    try:
        import rapfiles
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_file = f.name
            f.write("test content")
        
        try:
            # Test async read
            content = await rapfiles.read_file(test_file)
            # Test async write
            await rapfiles.write_file(test_file, "new content")
            return True
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.unlink(test_file)
    except ImportError:
        raise ImportError("rapfiles not installed. Install with: pip install rapfiles")


async def test_aiosqlite():
    """Test aiosqlite library (for comparison - likely fake async)."""
    try:
        import aiosqlite
        import tempfile
        import os
        
        test_db = tempfile.mktemp(suffix='.db')
        try:
            async with aiosqlite.connect(test_db) as db:
                await db.execute("CREATE TABLE test (id INTEGER)")
                await db.commit()
            return True
        finally:
            if os.path.exists(test_db):
                os.unlink(test_db)
    except ImportError:
        raise ImportError("aiosqlite not installed. Install with: pip install aiosqlite")


async def test_asyncio_files():
    """Test standard asyncio file I/O (wraps blocking I/O in threads)."""
    import tempfile
    import os
    
    test_file = tempfile.mktemp(suffix='.txt')
    try:
        # Use asyncio.to_thread for blocking I/O (this is fake async)
        def write_file():
            with open(test_file, 'w') as f:
                f.write("test")
        
        def read_file():
            with open(test_file, 'r') as f:
                return f.read()
        
        await asyncio.to_thread(write_file)
        await asyncio.to_thread(read_file)
        return True
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


LIBRARY_TESTS = {
    "rapfiles": test_rapfiles,
    "aiosqlite": test_aiosqlite,
    "asyncio-files": test_asyncio_files,
}

