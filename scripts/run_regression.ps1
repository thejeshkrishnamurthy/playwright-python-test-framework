$ErrorActionPreference = "Stop"

python database\initialise_database.py

python -m pytest `
    -m "regression or integration or bdd or accessibility" `
    --browser chromium `
    -n 2 `
    -v