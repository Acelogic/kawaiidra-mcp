#!/usr/bin/env python3
"""Wrapper script to run the Kawaiidra MCP server."""
import os
import sys
import asyncio
from pathlib import Path

# Windows-specific: use ProactorEventLoop for better subprocess/pipe handling
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import JPype before the MCP stdio event loop starts only when bridge mode is
# explicitly enabled. On Windows, lazy-importing JPype from inside an MCP tool
# handler can deadlock the stdio server, but importing it when bridge mode is
# disabled makes the stable subprocess path depend on JPype unnecessarily.
if os.environ.get("KAWAIIDRA_USE_BRIDGE", "true").lower() == "true":
    try:
        import jpype  # noqa: F401
    except ImportError:
        pass

# Run the server
from kawaiidra_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
