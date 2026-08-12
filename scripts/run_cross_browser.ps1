$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Running cross-browser smoke suite..."

python -m pytest `
    tests\ui `
    -m smoke `
    --browser chromium `
    --browser firefox `
    --browser webkit `
    -v

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Cross-browser suite PASSED."