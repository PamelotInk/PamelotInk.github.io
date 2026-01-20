# Start automated email alerts - checks every 5 minutes for significant results
# Run this from the project root

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $scriptRoot 'venv\Scripts\python.exe'
$emailScript = Join-Path $scriptRoot 'email_results.py'

Write-Host "📧 Starting Experiment Email Alerts" -ForegroundColor Green
Write-Host "Checking for significant results every 5 minutes..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

# Initial check
Write-Host "Running initial check..."
& $pythonExe $emailScript

# Loop every 5 minutes
while ($true) {
    Start-Sleep -Seconds 300  # 5 minutes
    
    Write-Host "`n--- New Check ($(Get-Date -Format 'HH:mm:ss')) ---" -ForegroundColor Cyan
    & $pythonExe $emailScript
}
