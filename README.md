# mcp-groupdocs-cloud

A lightweight MCP (Model Context Protocol) server that wraps GroupDocs Cloud functionality.

This repository contains a small Python-based MCP server used to expose GroupDocs Cloud capabilities via a simple local server for development, testing, and integration. The code is located in the `src/` folder (`server.py`, `server_models.py`) and a minimal test runner is provided in `src/test.py`.

## Requirements
- Obtain your GroupDocs Cloud API credentials (ClientId and ClientSecret) at https://dashboard.groupdocs.cloud/#/applications
- Python 3.10+ (recommend using a virtual environment)
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Quick start (local)

1. Clone the repo and change into it.
2. (Optional) Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables (if your server uses any external API keys). This project may integrate with GroupDocs Cloud APIs — if so, set your credentials in environment variables or a secrets store. Reasonable example variables (adjust to your code):

```bash
export GROUPDOCS_CLIENT_ID="your-client-id"
export GROUPDOCS_CLIENT_SECRET="your-client-secret"
export MCP_PORT=8080
```

4. Run the server locally. The repository contains `src/server.py` which can be started directly:

```bash
python ./src/server.py
```

Note: If your `server.py` uses a framework like Flask or FastAPI and requires a specific runner (e.g., `uvicorn`), start it as appropriate for that framework. Check `src/server.py` for the exact entrypoint.

## How to use

- Inspect `src/server.py` and `src/server_models.py` to see the available endpoints or handlers and the expected request/response models.
- The server is designed to act as an MCP worker — connect an MCP-aware client to it and exchange the protocol messages defined by your integration.

Because implementations differ, this README intentionally avoids hardcoding endpoint examples. See the source files for the canonical contract.

## Docker

There is a `Dockerfile` in the repo. You can build and run the container locally if you prefer containerized development. Example:

```bash
docker build -t mcp-groupdocs-cloud .
docker run -e GROUPDOCS_CLIENT_ID=... -e GROUPDOCS_CLIENT_SECRET=... -p 8080:8080 mcp-groupdocs-cloud
```

Adjust environment variables or ports to match your server’s configuration.

## License

See the `LICENSE` file at the repository root.

## Contact

If you need help understanding the code, open an issue or contact the project maintainers.

