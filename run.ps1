# Read .env file and set environment variables
Get-Content .env | foreach {
  $name, $value = $_.split('=')
  if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
    # skip empty or comment line in ENV file
    return
  }
  Set-Content env:\$name $value
}

# Optional: print them for verification
Write-Host "Environment variables loaded:"
Write-Host "CLIENT_ID=$env:CLIENT_ID"
Write-Host "CLIENT_SECRET=$env:CLIENT_SECRET"
Write-Host "MCP_PORT=$env:MCP_PORT"

# Run the Python script
python src/server.py