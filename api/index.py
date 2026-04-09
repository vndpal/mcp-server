"""Vercel serverless entrypoint for the SentinelScan Cloud MCP Server.

Vercel's Python runtime looks for a module-level ASGI `app` in files under
the `api/` directory and serves it as a serverless function. This file
imports the FastMCP instance defined in `server.py` and exposes its
Streamable-HTTP Starlette app.
"""

import os
import sys

# Make the repository root importable so we can `import server`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import mcp  # noqa: E402

# Vercel's Python runtime will serve this ASGI application.
app = mcp.streamable_http_app()
