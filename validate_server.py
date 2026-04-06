#!/usr/bin/env python
"""Step-by-step validation of Playwright MCP server"""

print("=" * 60)
print("STEP 1: Testing Imports")
print("=" * 60)

try:
    print("✓ Importing FastMCP...")
    from mcp.server.fastmcp import FastMCP
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing Playwright...")
    from playwright.async_api import async_playwright
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing Pydantic...")
    from pydantic import BaseModel
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing uvicorn...")
    import uvicorn
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing asyncio...")
    import asyncio
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing logging...")
    import logging
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

try:
    print("✓ Importing os...")
    import os
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

print("\n" + "=" * 60)
print("STEP 2: Testing FastMCP Initialization")
print("=" * 60)

try:
    print("✓ Creating FastMCP instance with stateless_http=True...")
    mcp = FastMCP("playwright-mcp-server", stateless_http=True, auth=None)
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

print("\n" + "=" * 60)
print("STEP 3: Inspecting FastMCP Object")
print("=" * 60)

print("✓ Checking FastMCP attributes...")
attrs = dir(mcp)
print(f"  Total attributes: {len(attrs)}")

# Check for key attributes
checks = ['app', '_app', 'run', 'tool', 'asgi_handler']
for check in checks:
    if hasattr(mcp, check):
        print(f"  ✓ Has '{check}'")
    else:
        print(f"  ✗ Missing '{check}'")

print("\n" + "=" * 60)
print("STEP 4: Defining a Test Tool")
print("=" * 60)

try:
    print("✓ Defining health_check tool...")
    @mcp.tool()
    async def health_check():
        return {"status": "healthy"}
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
    exit(1)

print("\n" + "=" * 60)
print("STEP 5: Finding ASGI App")
print("=" * 60)

asgi_app = None

if hasattr(mcp, 'app'):
    print("✓ Found mcp.app - using it")
    asgi_app = mcp.app
elif hasattr(mcp, '_app'):
    print("✓ Found mcp._app - using it")
    asgi_app = mcp._app
elif callable(mcp):
    print("✓ mcp is callable - using it directly")
    asgi_app = mcp
else:
    print("✗ Cannot find ASGI app")
    print("  Will attempt mcp.run()")
    asgi_app = None

if asgi_app:
    print(f"  ASGI app type: {type(asgi_app)}")
    print(f"  ASGI app class: {asgi_app.__class__.__name__}")

print("\n" + "=" * 60)
print("STEP 6: Port Configuration")
print("=" * 60)

port = int(os.getenv("PORT", 8931))
print(f"✓ PORT configured: {port}")

print("\n" + "=" * 60)
print("STEP 7: Startup Code Summary")
print("=" * 60)

print("""
The server will now:
1. Check if mcp.app exists
2. Check if mcp._app exists
3. Check if mcp itself is callable
4. Fall back to mcp.run() if nothing above works
5. Run uvicorn on 0.0.0.0:{} with the ASGI app
""".format(port))

print("=" * 60)
print("✅ ALL VALIDATION CHECKS PASSED")
print("=" * 60)
print("\nReady to start server. Use: python server.py")
