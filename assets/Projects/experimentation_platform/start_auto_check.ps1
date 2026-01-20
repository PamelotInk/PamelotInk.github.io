# Auto-check experiments every 5 minutes and save results to files
# No email password needed!

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $scriptRoot 'venv\Scripts\python.exe'
$checkScript = Join-Path $scriptRoot 'check_results.py'

Write-Host "📊 Starting Experiment Results Auto-Checker" -ForegroundColor Green
Write-Host "Checking every 5 minutes and saving to experiment_results.txt" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

# Initial check
Write-Host "Running initial check..."
& $pythonExe $checkScript

# Loop every 5 minutes
while ($true) {
    Start-Sleep -Seconds 300  # 5 minutes
    
    Write-Host "`n--- New Check ($(Get-Date -Format 'HH:mm:ss')) ---" -ForegroundColor Cyan
    & $pythonExe $checkScript
}
