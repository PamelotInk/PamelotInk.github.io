# Start Streamlit in background and write PID to streamlit.pid
# Run this from the project root (where app.py and venv/ live)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$streamlitExe = Join-Path $scriptRoot 'venv\Scripts\streamlit.exe'

if (-not (Test-Path $streamlitExe)) {
    Write-Error "streamlit.exe not found at $streamlitExe. Activate venv or check your path."
    exit 1
}

# Prepare log/err files (overwrite each start)
$log = Join-Path $scriptRoot 'streamlit.log'
$err = Join-Path $scriptRoot 'streamlit.err'
"" | Out-File -FilePath $log -Encoding utf8
"" | Out-File -FilePath $err -Encoding utf8

# Start Streamlit directly and redirect stdout/stderr to files (clean quoting)
$appPath = Join-Path $scriptRoot 'app.py'

# Use Start-Process with redirection so paths with spaces are handled correctly
# Prefer launching via the venv python to avoid issues with the streamlit.exe wrapper
$pythonExe = Join-Path $scriptRoot 'venv\Scripts\python.exe'
$arguments = "-m streamlit run `"$appPath`" --server.headless true --server.port 8501"
$proc = Start-Process -FilePath $pythonExe -ArgumentList $arguments -RedirectStandardOutput $log -RedirectStandardError $err -WindowStyle Hidden -PassThru

# Save PID for later stopping
$pidFile = Join-Path $scriptRoot 'streamlit.pid'
$proc.Id | Out-File -FilePath $pidFile -Encoding ascii

Write-Host "Started Streamlit (PID $($proc.Id)). Logs: $log / $err"
Write-Host "Open http://localhost:8501 in your browser to view the app."