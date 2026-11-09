# PowerShell wrapper to cleanly package lambda-package.zip using Python standard zipfile
$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "rebuild_clean_lambda.py"
Write-Host "Rebuilding lambda-package.zip using $scriptPath..."
python $scriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to rebuild lambda package"
} else {
    Write-Host "lambda-package.zip built successfully!"
}
