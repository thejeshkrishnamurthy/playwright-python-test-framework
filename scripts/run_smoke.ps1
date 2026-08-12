$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Running Playwright smoke pipeline..."

python -m ruff check .

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

python -m pytest `
    -m "smoke or api" `
    --browser chromium `
    -n 2 `
    -v

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Smoke pipeline PASSED."