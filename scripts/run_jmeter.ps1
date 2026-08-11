$ErrorActionPreference = "Stop"

$JmeterCommand = "C:\Program Files\apache-jmeter-5.6.3\bin\jmeter.bat"

$TestPlan = "performance\booking-api.jmx"
$ResultFile = "reports\jmeter\results.jtl"
$HtmlReport = "reports\jmeter\html"

Write-Host "Cleaning previous JMeter results..."

Remove-Item `
    -Recurse `
    -Force `
    $HtmlReport `
    -ErrorAction SilentlyContinue

Remove-Item `
    -Force `
    $ResultFile `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Force `
    "reports\jmeter" |
    Out-Null

Write-Host "Starting JMeter performance test..."

& $JmeterCommand `
    -n `
    -t $TestPlan `
    -l $ResultFile `
    -e `
    -o $HtmlReport

if ($LASTEXITCODE -ne 0) {
    throw "JMeter execution failed."
}

Write-Host "JMeter execution completed successfully."
Write-Host "Report:"
Write-Host "$HtmlReport\index.html"