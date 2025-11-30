$envFile    = ".env"
$venvDir    = ".venv"
$markerFile = ".venv\.deps_installed"

# Load .env if present (optional)
if (Test-Path $envFile) {
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
    Write-Host "[init_mcp.ps1] Environment variables loaded from $envFile."
} else {
    Write-Host "[init_mcp.ps1] Warning: $envFile not found. Continuing without env variables..."
}

# Ensure python exists
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "[init_mcp.ps1] Python not found in PATH."
    exit 1
}

# Remove existing venv
if (Test-Path $venvDir) {
    Write-Host "[init_mcp.ps1] Removing existing virtual environment at $venvDir..."
    Remove-Item $venvDir -Recurse -Force
}

Write-Host "[init_mcp.ps1] Creating virtual environment in $venvDir..."
python -m venv $venvDir

Write-Host "[init_mcp.ps1] Activating virtual environment..."
. "$venvDir\Scripts\Activate.ps1"

if (-not (Test-Path "requirements.txt")) {
    Write-Error "[init_mcp.ps1] requirements.txt not found."
    exit 1
}

Write-Host "[init_mcp.ps1] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Mark deps as installed so run_mcp.ps1 can skip reinstall
New-Item -ItemType File -Path $markerFile -Force | Out-Null

Write-Host "[init_mcp.ps1] Initialization complete. You can now run .\run_mcp.ps1"
