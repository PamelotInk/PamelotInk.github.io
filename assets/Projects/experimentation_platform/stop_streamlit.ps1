# Stop Streamlit process started by start_streamlit.ps1
# Run this from the project root

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $scriptRoot 'streamlit.pid'

if (-not (Test-Path $pidFile)) {
    Write-Host "No PID file found at $pidFile. There may be no background Streamlit started with the helper."
    Write-Host "You can stop all streamlit processes with: Get-Process -Name streamlit | Stop-Process"
    exit 0
}

try {
    $processId = Get-Content $pidFile | Select-Object -First 1
    if ($processId -and (Get-Process -Id $processId -ErrorAction SilentlyContinue)) {
        # Kill all child processes first
        $children = Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $processId }
        foreach ($child in $children) {
            Stop-Process -Id $child.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped child process (PID $($child.ProcessId))"
        }
        
        # Then kill the main process
        Stop-Process -Id $processId -Force
        Remove-Item $pidFile -ErrorAction SilentlyContinue
        Write-Host "Stopped Streamlit (PID $processId) and all child processes."
    } else {
        Write-Host "Process with PID $processId not found. Cleaning up PID file." 
        Remove-Item $pidFile -ErrorAction SilentlyContinue
    }
} catch {
    Write-Error "Error stopping Streamlit: $_"
}
