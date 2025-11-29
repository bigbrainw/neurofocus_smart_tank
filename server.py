#!/usr/bin/env python3
"""Entry point for Docker builds - delegates to src.main:main"""

from src.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

