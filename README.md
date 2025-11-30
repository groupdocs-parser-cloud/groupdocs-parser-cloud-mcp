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

## 2. Configure environment variables

Create a `.env` file with your settings.  
You can either create it manually or copy the `.env.example` file.

```
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
MCP_PORT=8000
```

Get credentials at:  
https://dashboard.groupdocs.cloud/#/applications

## 3. Run the server

### Bash / macOS / Linux
```bash
./run.sh
```

### Windows (PowerShell):
```powershell
.\run.ps1
```

### Windows (CMD):
```cmd
run.bat
```

Server starts at:

```
http://localhost:8000/mcp
```

---

# 🧩 How to use the MCP server in your environments, agents, and assistants

This section describes integration examples.

---

## Test with @modelcontextprotocol/inspector

1. Run the inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```
2. In the browser:
   - Select **“streamable HTTP”**
   - Enter your MCP URL:
     ```
     http://127.0.0.1:8000/mcp
     ```
   - Click **Connect**


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

# Troubleshooting and Advanced Options

## Reinitialize the Virtual Environment

If you update the codebase and the MCP server stops working due to missing dependencies (for example, after adding new packages to `requirements.txt`), you may need to **fully reinitialize** the local virtual environment.

To do this, use the `init_mcp` script for your platform:

### Linux / macOS / Bash
```bash
./init_mcp.sh
```

### Windows PowerShell
```powershell
.\init_mcp.ps1
```

### Windows CMD
```cmd
init_mcp.bat
```

### What this command does
The `init_mcp` script performs a full reset:

1. Removes the existing `.venv` directory  
2. Creates a fresh virtual environment  
3. Installs all dependencies from `requirements.txt`  
4. Prepares the environment so `run_mcp.*` can start the server normally

After reinitialization, simply start the server again:

### Bash / macOS / Linux
```bash
./run_mcp.sh
```

### PowerShell
```powershell
.\run_mcp.ps1
```

### CMD
```cmd
run_mcp.bat
```

This ensures your environment is always in sync with the current project requirements.

# 📄 License

This project is licensed under **MIT License**.
