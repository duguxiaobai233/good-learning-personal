$ErrorActionPreference = 'Stop'

$runtimeRoot = 'C:\Users\sora\Documents\Codex\tools\good-learning'
$pythonExe = Join-Path $runtimeRoot 'venv\Scripts\python.exe'
$skillRoot = Split-Path -Parent $PSScriptRoot
$texCandidates = @(
    (Join-Path $runtimeRoot 'miktex\texmfs\install\miktex\bin\x64'),
    (Join-Path $runtimeRoot 'miktex\miktex\bin\x64')
)
$texBin = $texCandidates | Where-Object { Test-Path -LiteralPath (Join-Path $_ 'xelatex.exe') } | Select-Object -First 1
if (-not (Test-Path -LiteralPath $pythonExe)) { throw "Python environment is missing: $pythonExe" }
if (-not $texBin) { throw "MiKTeX environment is missing under $runtimeRoot" }

$oldPath = $env:PATH
$oldFont = $env:GOOD_LEARNING_FONT
try {
    $env:PATH = (Split-Path -Parent $pythonExe) + ';' + $texBin + ';' + $oldPath
    $env:GOOD_LEARNING_FONT = 'C:\Windows\Fonts\msyh.ttc'
    if ($args.Count -eq 1 -and $args[0] -eq '--check') {
        & $pythonExe -c "import sys,PIL,shutil; print('Python:',sys.version.split()[0]); print('Pillow:',PIL.__version__); print('XeLaTeX:',shutil.which('xelatex'))"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        & (Join-Path $texBin 'xelatex.exe') --version
        exit $LASTEXITCODE
    }
    $allowed = @('render_summary_map.py','render_study_pdf.py','compile_study_pdf.py')
    if ($args.Count -lt 1 -or [string]$args[0] -notin $allowed) {
        Write-Output 'Usage: run-local.ps1 <render_summary_map.py|render_study_pdf.py|compile_study_pdf.py> [arguments]'
        Write-Output 'Check environment: run-local.ps1 --check'
        exit 2
    }
    $scriptPath = Join-Path $skillRoot ('scripts\' + [string]$args[0])
    $forwardArgs = @($args | Select-Object -Skip 1)
    & $pythonExe $scriptPath @forwardArgs
    exit $LASTEXITCODE
}
finally {
    $env:PATH = $oldPath
    $env:GOOD_LEARNING_FONT = $oldFont
}
