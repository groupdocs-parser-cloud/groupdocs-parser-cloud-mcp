# GroupDocs.Parser Cloud MCP Server

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![GroupDocs.Cloud](https://img.shields.io/badge/GroupDocs-Cloud_API-orange.svg)]()
[![MCP Compatible](https://img.shields.io/badge/MCP-Model_Context_Protocol-purple.svg)]()

A lightweight **MCP (Model Context Protocol)** server that wraps **GroupDocs.Parser Cloud API** to provide document-parsing capabilities to AI agents, assistants, and development environments.

It enables LLMs to extract text, images, and barcodes from documents stored in GroupDocs Cloud storage, and provides shared cloud storage utilities (upload, download, list, exists, delete).

---

# 🔧 Features

- Lightweight GroupDocs.Parser Cloud MCP server
- Document parsing via GroupDocs.Parser Cloud:
  - Extract **plain text**
  - Extract **images** 
  - Extract **barcodes**  
- Supports 50+ document formats (PDF, Word, Excel, PowerPoint, emails, archives, images, and more)
- Cross-platform: Windows, macOS, Linux

# 🚀 Quick Start

This section explains how to configure and run the **GroupDocs.Parser Cloud MCP server** 

## 1. Clone the repository

```bash
git clone git@github.com:groupdocs-parser-cloud/groupdocs-parser-cloud-mcp.git
cd groupdocs-parser-cloud-mcp
```

## 2. Create and activate a virtual environment

### Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Configure environment variables

Create a `.env` file:

```
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
MCP_PORT=8000
```

Get credentials at:  
https://dashboard.groupdocs.cloud/#/applications

## 4. Run the server

### PowerShell
```powershell
.\run.ps1
```

### Bash / macOS / Linux
```bash
./run.sh
```

Server starts at:

```
http://localhost:8000/mcp
```

---

## 5. Test with @modelcontextprotocol/inspector

1. Run the inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```
2. In the browser:
   - Select **“streamable HTTP”**
   - Enter:
     ```
     http://localhost:8000/mcp
     ```
   - Click **Connect**


---

# 🧩 How to use the MCP server in your environments, agents, and assistants

This section describes real-world integration examples.

---

## 📘 Using the MCP server in VSCode

1. Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "groupdocs-parser-mcp-local": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

2. Restart VSCode if required.  
Now the MCP server is available inside VSCode’s MCP-enabled environments.

---

## 🤖 Using the MCP server with KiloCode

1. Open the project in VSCode  
2. Go to **KiloCode Settings → MCP Servers**  
3. Open the **Installed** tab  
4. Edit “Project MCP”  
5. Add the config:

```json
{
  "mcpServers": {
    "groupdocs-parser-mcp-local": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:8000/mcp",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

6. Add a test file such as `info.pdf`  
7. Example prompt:

> Extract text from `info.pdf` using groupdocs parser MCP and briefly summarize the document.

---

# 📄 License

This project is licensed under **MIT License**.
