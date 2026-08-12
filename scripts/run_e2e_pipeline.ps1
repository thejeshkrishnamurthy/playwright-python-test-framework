$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================="
Write-Host "     Playwright Python - End-to-End Quality Pipeline"
Write-Host "========================================================="
Write-Host ""

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$JmeterCommand = "C:\Program Files\apache-jmeter-5.6.3\bin\jmeter.bat"

$AllureResults = "reports\allure-results"
$JmeterResults = "reports\jmeter\results.jtl"
$JmeterHtml = "reports\jmeter\html"
$JmeterPlan = "performance\booking-api.jmx"

$FailureCount = 0


function Run-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "---------------------------------------------------------"
    Write-Host $Name
    Write-Host "---------------------------------------------------------"

    try {
        & $Command

        if ($LASTEXITCODE -ne 0) {
            throw "$Name failed with exit code $LASTEXITCODE"
        }

        Write-Host "[PASS] $Name"
    }
    catch {
        Write-Host "[FAIL] $Name"
        Write-Host $_
        throw
    }
}


# ---------------------------------------------------------
# STEP 1 - Environment validation
# ---------------------------------------------------------

Run-Step "STEP 1 - Validate Python environment" {

    python --version
    python -m pip --version

    python -c "
from playwright.sync_api import sync_playwright
print('Playwright import successful')
"
}


# ---------------------------------------------------------
# STEP 2 - Validate project configuration
# ---------------------------------------------------------

Run-Step "STEP 2 - Validate framework configuration" {

    python -c "
from utils.config import get_settings

settings = get_settings()

print('UI URL :', settings.ui_base_url)
print('API URL:', settings.api_base_url)
print('Configuration loaded successfully')
"
}


# ---------------------------------------------------------
# STEP 3 - Ruff
# ---------------------------------------------------------

Run-Step "STEP 3 - Ruff linting" {

    python -m ruff check .
}


# ---------------------------------------------------------
# STEP 4 - Black
# ---------------------------------------------------------

Run-Step "STEP 4 - Black formatting validation" {

    python -m black --check .
}


# ---------------------------------------------------------
# STEP 5 - Mypy
# ---------------------------------------------------------

Run-Step "STEP 5 - Static type checking" {

    python -m mypy `
        pages `
        api_clients `
        utils `
        database `
        models `
        tests
}


# ---------------------------------------------------------
# STEP 6 - Initialise local database
# ---------------------------------------------------------

Run-Step "STEP 6 - Initialise SQLite database" {

    python database\initialise_database.py

    if (-not (Test-Path "database\test_data.db")) {
        throw "SQLite database was not created"
    }

    Write-Host "SQLite database ready."
}


# ---------------------------------------------------------
# STEP 7 - Test discovery
# ---------------------------------------------------------

Run-Step "STEP 7 - Pytest test discovery" {

    python -m pytest --collect-only -q
}


# ---------------------------------------------------------
# STEP 8 - API tests
# ---------------------------------------------------------

Run-Step "STEP 8 - Execute API tests" {

    python -m pytest `
        tests\api `
        -m api `
        -v
}


# ---------------------------------------------------------
# STEP 9 - UI smoke tests
# ---------------------------------------------------------

Run-Step "STEP 9 - Execute Chromium UI smoke tests" {

    python -m pytest `
        tests\ui `
        -m smoke `
        --browser chromium `
        -v
}


# ---------------------------------------------------------
# STEP 10 - Integration / Database tests
# ---------------------------------------------------------

Run-Step "STEP 10 - Execute integration tests" {

    python -m pytest `
        tests\integration `
        -v
}


# ---------------------------------------------------------
# STEP 11 - BDD tests
# ---------------------------------------------------------

Run-Step "STEP 11 - Execute BDD tests" {

    python -m pytest `
        tests\bdd `
        --browser chromium `
        -v
}


# ---------------------------------------------------------
# STEP 12 - Accessibility tests
# ---------------------------------------------------------

Run-Step "STEP 12 - Execute accessibility tests" {

    python -m pytest `
        tests\accessibility `
        -m accessibility `
        --browser chromium `
        -v
}


# ---------------------------------------------------------
# STEP 13 - Parallel regression
# ---------------------------------------------------------

Run-Step "STEP 13 - Execute regression tests in parallel" {

    python -m pytest `
        -m "regression" `
        --browser chromium `
        -n 2 `
        -v
}


# ---------------------------------------------------------
# STEP 14 - Cross-browser smoke tests
# ---------------------------------------------------------

Run-Step "STEP 14 - Cross-browser smoke execution" {

    python -m pytest `
        tests\ui `
        -m smoke `
        --browser chromium `
        --browser firefox `
        --browser webkit `
        -v
}


# ---------------------------------------------------------
# STEP 15 - Complete framework test
# ---------------------------------------------------------

Run-Step "STEP 15 - Complete framework execution" {

    python -m pytest `
        --browser chromium `
        -n 2 `
        -v
}


# ---------------------------------------------------------
# STEP 16 - Verify Allure results
# ---------------------------------------------------------

Run-Step "STEP 16 - Validate Allure results" {

    if (-not (Test-Path $AllureResults)) {
        throw "Allure results directory does not exist."
    }

    $ResultFiles = Get-ChildItem $AllureResults -Filter "*-result.json"

    if ($ResultFiles.Count -eq 0) {
        throw "No Allure result files found."
    }

    Write-Host "Allure results found:"
    Write-Host $ResultFiles.Count
}


# ---------------------------------------------------------
# STEP 17 - JMeter performance testing
# ---------------------------------------------------------

if (Test-Path $JmeterCommand) {

    Write-Host ""
    Write-Host "---------------------------------------------------------"
    Write-Host "STEP 17 - JMeter Performance Test"
    Write-Host "---------------------------------------------------------"

    Remove-Item `
        -Recurse `
        -Force `
        $JmeterHtml `
        -ErrorAction SilentlyContinue

    Remove-Item `
        -Force `
        $JmeterResults `
        -ErrorAction SilentlyContinue

    New-Item `
        -ItemType Directory `
        -Force `
        "reports\jmeter" |
        Out-Null

    & $JmeterCommand `
        -n `
        -t $JmeterPlan `
        -l $JmeterResults `
        -e `
        -o $JmeterHtml

    if ($LASTEXITCODE -ne 0) {
        throw "JMeter execution failed."
    }

    if (-not (Test-Path "$JmeterHtml\index.html")) {
        throw "JMeter HTML report was not generated."
    }

    Write-Host "[PASS] JMeter performance testing"
}
else {

    Write-Host ""
    Write-Host "[SKIPPED] JMeter"
    Write-Host "JMeter executable not found at:"
    Write-Host $JmeterCommand
}


# ---------------------------------------------------------
# Final result
# ---------------------------------------------------------

Write-Host ""
Write-Host "========================================================="
Write-Host "              PIPELINE COMPLETED SUCCESSFULLY"
Write-Host "========================================================="
Write-Host ""

Write-Host "Validated:"
Write-Host "  [OK] Python environment"
Write-Host "  [OK] Framework configuration"
Write-Host "  [OK] Ruff"
Write-Host "  [OK] Black"
Write-Host "  [OK] mypy"
Write-Host "  [OK] SQLite"
Write-Host "  [OK] Test discovery"
Write-Host "  [OK] API testing"
Write-Host "  [OK] UI testing"
Write-Host "  [OK] Integration testing"
Write-Host "  [OK] BDD"
Write-Host "  [OK] Accessibility"
Write-Host "  [OK] Parallel regression"
Write-Host "  [OK] Cross-browser execution"
Write-Host "  [OK] Allure results"

if (Test-Path "$JmeterHtml\index.html") {
    Write-Host "  [OK] JMeter performance testing"
}

Write-Host ""
Write-Host "Allure results:"
Write-Host "$ProjectRoot\$AllureResults"

if (Test-Path "$JmeterHtml\index.html") {
    Write-Host ""
    Write-Host "JMeter report:"
    Write-Host "$ProjectRoot\$JmeterHtml\index.html"
}

Write-Host ""