Param(
    [Parameter(Mandatory=$true)] [string]$PfxPath,
    [Parameter(Mandatory=$true)] [string]$PfxPassword,
    [string]$TimestampUrl = "http://timestamp.digicert.com",
    [string]$ExePath = "dist\\StandaloneMacro.exe",
    [string]$InstallerPath = "installer\\output\\StandaloneMacroSetup.exe"
)

$signTool = (Get-Command signtool.exe -ErrorAction SilentlyContinue).Source
if (-not $signTool) {
    throw "signtool.exe niet gevonden. Installeer Windows SDK / Build Tools."
}

$targets = @($ExePath, $InstallerPath)
foreach ($target in $targets) {
    if (Test-Path $target) {
        & $signTool sign /fd SHA256 /tr $TimestampUrl /td SHA256 /f $PfxPath /p $PfxPassword $target
        if ($LASTEXITCODE -ne 0) {
            throw "Ondertekenen mislukt voor: $target"
        }
        Write-Host "Ondertekend: $target"
    } else {
        Write-Warning "Bestand niet gevonden, overgeslagen: $target"
    }
}
