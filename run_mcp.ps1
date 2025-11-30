$envFile    = ".env"
$venvDir    = ".venv"
$markerFile = ".venv\.deps_installed"

if (-not (Test-Path $envFile)) {
    Write-Error "[run_mcp.ps1] .env file not found. Create it before running this script."
    exit 1
}

# Load .env variables (skip empty or comment lines)
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -eq "" -or $line.StartsWith("#")) { return }

    $parts = $line.Split("=", 2)
    if ($parts.Count -eq 2) {
        $name  = $parts[0].Trim()
        $value = $parts[1].Trim()
        if ($name) {
            Set-Item "Env:$name" $value
        }
    }
}

Write-Host "[run_mcp.ps1] Environment variables loaded."

# Ensure python exists
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "[run_mcp.ps1] Python not found in PATH."
    exit 1
}

# Create venv
if (-not (Test-Path $venvDir)) {
    Write-Host "[run_mcp.ps1] Creating virtual environment..."
    python -m venv $venvDir
}

Write-Host "[run_mcp.ps1] Activating virtual environment..."
. "$venvDir\Scripts\Activate.ps1"

# Install requirements
if (-not (Test-Path $markerFile)) {
    if (-not (Test-Path "requirements.txt")) {
        Write-Error "[run_mcp.ps1] requirements.txt not found."
        exit 1
    }
    Write-Host "[run_mcp.ps1] Installing dependencies..."
    pip install -r requirements.txt
    New-Item -ItemType File -Path $markerFile -Force | Out-Null
    Write-Host "[run_mcp.ps1] Dependencies installed."
}

Write-Host "[run_mcp.ps1] Starting MCP server..."
python src/server.py
