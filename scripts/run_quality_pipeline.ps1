$ErrorActionPreference = "Stop"

Write-Host "Step 1: Running Ruff"
python -m ruff check .

Write-Host "Step 2: Checking Black formatting"
python -m black --check .

Write-Host "Step 3: Running mypy"
python -m mypy pages api_clients utils database models tests

Write-Host "Step 4: Checking test collection"
python -m pytest --collect-only -q

Write-Host "Step 5: Initialising SQLite database"
python database\initialise_database.py

Write-Host "Step 6: Running API and smoke tests"
python -m pytest `
    -m "api or smoke" `
    --browser chromium `
    -n 2 `
    -v

Write-Host "Quality pipeline completed successfully."