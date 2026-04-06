# Playwright MCP Server

A Model Context Protocol (MCP) server for browser automation using Playwright. This server provides a set of tools for controlling a headless Chromium browser, perfect for automated testing, web scraping, and browser-based workflows.

## Features

- **Lazy-loaded browser** - Browser initializes on first tool call, not at startup
- **Full browser automation** - Navigate, click, type, take screenshots, evaluate JavaScript, and more
- **Azure App Service ready** - Health check endpoint for Azure Service Health Probes
- **Async/await support** - Efficient asynchronous operations with FastMCP
- **Streamable HTTP transport** - Enables real-time communication with clients

## Tools Available

| Tool | Description | Input |
|------|-------------|-------|
| `health_check()` | Returns server health status | None |
| `browser_navigate()` | Navigate to a URL | `url: str` |
| `browser_navigate_back()` | Go back in browser history | None |
| `browser_click()` | Click an element | `ref: str` (CSS selector) |
| `browser_drag()` | Drag and drop between elements | `startRef`, `endRef` |
| `browser_hover()` | Hover over an element | `ref: str` |
| `browser_type()` | Type text into an element | `ref: str`, `text: str` |
| `browser_fill_form()` | Fill multiple form fields | `fields: list` |
| `browser_file_upload()` | Upload files to a file input | `files: list` |
| `browser_press_key()` | Press a keyboard key | `key: str` |
| `browser_resize()` | Resize the browser window | `width: int`, `height: int` |
| `browser_console_messages()` | Retrieve page console messages | `level: str` |
| `browser_handle_dialog()` | Handle alerts/prompts/confirmations | `accept: bool` |
| `browser_evaluate()` | Execute JavaScript in page context | `function: str` |
| `browser_snapshot()` | Capture page DOM/accessibility snapshot | `url: str` (optional) |
| `browser_network_requests()` | Get network requests made by the page | `static: bool`, `requestBody: bool`, `requestHeaders: bool` |
| `browser_run_code()` | Execute custom Playwright code | `code: str`, `filename: str` |
| `browser_select_option()` | Select option(s) from a dropdown | `ref: str`, `values: list` |
| `browser_tabs()` | Manage browser tabs | `action: str` |
| `browser_wait_for()` | Wait for text, element, or timeout | Depends on parameters |
| `browser_take_screenshot()` | Take a screenshot | `filename: str`, `fullPage: bool` |
| `browser_close()` | Close the browser | None |

## Prerequisites

- Python 3.8+
- pip or conda

## Installation

1. **Clone or download this project**

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

```bash
python server.py
```

The server will start on `http://0.0.0.0:8000` by default.

### Custom Port

Set the `PORT` environment variable to use a different port:

```bash
# Windows
set PORT=3000
python server.py

# Linux/macOS
export PORT=3000
python server.py
```

## Usage Example

Once the server is running, you can call the MCP tools via HTTP:

```bash
curl -X POST http://localhost:8000/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Deployment to Azure

### Prerequisites
- Azure CLI installed
- An Azure subscription
- Docker (optional, for containerization)

### Using Azure App Service

1. **Create an App Service**
   ```bash
   az appservice plan create --name <plan-name> --resource-group <rg-name> --sku B1 --is-linux
   az webapp create --resource-group <rg-name> --plan <plan-name> --name <app-name> --runtime "PYTHON:3.11"
   ```

2. **Deploy the app**
   ```bash
   az webapp up --resource-group <rg-name> --name <app-name> --runtime "PYTHON:3.11"
   ```

3. **Configure environment**
   ```bash
   az webapp config appsettings set --resource-group <rg-name> --name <app-name> --settings PORT=8000
   ```

### Docker Deployment (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && playwright install chromium

COPY . .

EXPOSE 8000

CMD ["python", "server.py"]
```

Build and run:
```bash
docker build -t playwright-mcp-server .
docker run -p 8000:8000 playwright-mcp-server
```

## Environment Variables

- `PORT` - Port to run the server on (default: 8000)

## Testing

Run the test suite:
```bash
python test_fastmcp_simple.py
```

Validate dependencies:
```bash
python validate_server.py
```

## Project Structure

```
.
├── server.py              # Main MCP server application
├── requirements.txt       # Python dependencies
├── test_fastmcp_simple.py # Test suite
├── validate_server.py     # Dependency validation
├── README.md              # This file
└── .venv/                 # Virtual environment (auto-generated)
```

## Notes

- The browser instance is lazy-loaded on the first tool call and reused for subsequent calls
- Browser tabs/contexts are maintained during the server lifetime
- The server includes a health check endpoint (`/health_check`) for Azure App Service monitoring
- Screenshots are saved to the working directory or specified path
- JavaScript evaluation runs in the context of the current page

## Troubleshooting

**Browser won't initialize:**
- Ensure Playwright chromium is installed: `playwright install chromium`
- Check system dependencies are installed (Linux/macOS)

**Port already in use:**
- Change the PORT environment variable to an available port

**Timeout errors:**
- Increase browser timeout or check network connectivity to target URLs

## License

[Your License Here]

## Support

For issues or questions, please refer to:
- [Playwright Documentation](https://playwright.dev/python/)
- [FastMCP Documentation](https://github.com/pydantic/fastmcp)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
