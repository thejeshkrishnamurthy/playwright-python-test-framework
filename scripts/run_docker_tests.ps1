$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Checking Docker..."

docker info *> $null

if ($LASTEXITCODE -ne 0) {
    throw "Docker engine is not running."
}

Write-Host "Building Playwright image..."

docker build `
    -t playwright_python_fw .

if ($LASTEXITCODE -ne 0) {
    throw "Docker build failed."
}

Write-Host "Running automation container..."

docker run `
    --rm `
    --env-file .env `
    -v "${PWD}\reports:/framework/reports" `
    -v "${PWD}\test-results:/framework/test-results" `
    playwright_python_fw

if ($LASTEXITCODE -ne 0) {
    throw "Docker test execution failed."
}

Write-Host ""
Write-Host "Docker automation PASSED."