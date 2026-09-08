# PowerShell script to update lambda-package.zip with the latest index.js and fonts
$ErrorActionPreference = "Stop"

$zipPath = Join-Path $PSScriptRoot "..\lambda-package.zip"
$indexPath = Join-Path $PSScriptRoot "..\index.js"
$fontPath = Join-Path $PSScriptRoot "..\fonts\NotoSansTC-Regular.ttf"

Write-Host "Checking target files..."
if (-not (Test-Path $zipPath)) {
    Write-Error "lambda-package.zip not found at $zipPath"
}
if (-not (Test-Path $indexPath)) {
    Write-Error "index.js not found at $indexPath"
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

Write-Host "Opening $zipPath in Update mode..."
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Update)

try {
    # 1. Update index.js
    $indexEntry = $zip.GetEntry("index.js")
    if ($null -ne $indexEntry) {
        Write-Host "Removing existing index.js from zip..."
        $indexEntry.Delete()
    }
    Write-Host "Adding latest index.js to zip..."
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $indexPath, "index.js", [System.IO.Compression.CompressionLevel]::Optimal)

    # 2. Check or update fonts/NotoSansTC-Regular.ttf
    $fontEntry = $zip.GetEntry("fonts/NotoSansTC-Regular.ttf")
    if ($null -eq $fontEntry) {
        $fontEntry = $zip.GetEntry("fonts\NotoSansTC-Regular.ttf")
    }
    if ($null -eq $fontEntry -and (Test-Path $fontPath)) {
        Write-Host "Adding fonts/NotoSansTC-Regular.ttf to zip..."
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $fontPath, "fonts/NotoSansTC-Regular.ttf", [System.IO.Compression.CompressionLevel]::Optimal)
    } else {
        Write-Host "fonts/NotoSansTC-Regular.ttf exists in zip."
    }
}
finally {
    $zip.Dispose()
    Write-Host "Zip archive updated and closed successfully."
}

# Verify the update
$verifyZip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $idx = $verifyZip.GetEntry("index.js")
    Write-Host "Verification:"
    Write-Host "  Entry: $($idx.FullName)"
    Write-Host "  Length: $($idx.Length) bytes"
    Write-Host "  CompressedLength: $($idx.CompressedLength) bytes"
    Write-Host "  LastWriteTime: $($idx.LastWriteTime)"
}
finally {
    $verifyZip.Dispose()
}

Write-Host "✅ lambda-package.zip packaging completed successfully!"
