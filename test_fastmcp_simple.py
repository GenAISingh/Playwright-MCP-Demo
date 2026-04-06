#!/usr/bin/env python
"""Minimal FastMCP server test"""
import os
os.environ["PORT"] = "8931"

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server", stateless_http=True, auth=None)

@mcp.tool()
async def hello():
    """Simple test tool"""
    return {"message": "hello"}

if __name__ == "__main__":
    print("Starting FastMCP server...")
    try:
        mcp.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
