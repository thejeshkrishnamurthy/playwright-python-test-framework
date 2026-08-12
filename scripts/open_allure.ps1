$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$ResultDirectory =
    "reports\allure-results"

if (-not (Test-Path $ResultDirectory)) {
    throw "Allure results folder does not exist."
}

$Results =
    Get-ChildItem `
        $ResultDirectory `
        -Filter "*-result.json"

if ($Results.Count -eq 0) {
    throw "No Allure results found. Run pytest first."
}

Write-Host "Opening Allure report..."

allure serve $ResultDirectory