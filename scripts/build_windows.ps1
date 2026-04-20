Param(
    [string]$AppName = "StandaloneMacro",
    [string]$VersionFile = "windows/version_info.txt",
    [string]$EntryScript = "macro_app.py"
)

$pyiArgs = @(
    "--noconfirm",
    "--clean",
    "--windowed",
    "--onefile",
    "--name", $AppName,
    "--version-file", $VersionFile,
    $EntryScript
)

if (Test-Path "assets/app.ico") {
    $pyiArgs = @("--icon", "assets/app.ico") + $pyiArgs
}

Write-Host "Running: pyinstaller $($pyiArgs -join ' ')"
& pyinstaller @pyiArgs
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed with exit code $LASTEXITCODE"
}
