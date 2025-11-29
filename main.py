#!/usr/bin/env python3
"""Entry point for Docker builds - delegates to server.py which has runtime injection"""

# Import server to trigger any injected runtime environment loader code
# Then execute the same logic
from src.main import main
import asyncio

if __name__ == "__main__":
    # Import server module first to ensure injected code runs
    import server  # noqa: F401
    # Then run the actual main function
    asyncio.run(main())

