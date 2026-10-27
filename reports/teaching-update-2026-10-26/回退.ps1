param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot '变更清单与校验值.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$live = $manifest.installed_root
$backup = Join-Path $PSScriptRoot '修改前完整版本'
$changes = @()
foreach ($name in $manifest.changed_files) {
    $source = Join-Path $backup $name
    $target = Join-Path $live $name
    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
    $targetHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
    $beforeHash = $manifest.before_sha256.PSObject.Properties[$name].Value
    $afterHash = $manifest.after_sha256.PSObject.Properties[$name].Value
    if ($sourceHash -ne $beforeHash) { throw "Backup file changed: $name" }
    if ($targetHash -eq $beforeHash) { continue }
    if ($targetHash -ne $afterHash) { throw "Later changes detected; review before rollback: $name" }
    $changes += [PSCustomObject]@{ Source = $source; Target = $target; Name = $name }
}
if (-not $Apply) {
    Write-Output "Rollback preflight passed. Files requiring restoration: $($changes.Count)."
    Write-Output 'No files modified. Run this script with -Apply only when you want to restore this version.'
    exit 0
}
foreach ($entry in $changes) {
    Copy-Item -LiteralPath $entry.Source -Destination $entry.Target -Force
    $expected = $manifest.before_sha256.PSObject.Properties[$entry.Name].Value
    $actual = (Get-FileHash -LiteralPath $entry.Target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $expected) { throw "Restore verification failed: $($entry.Name)" }
}
Write-Output "Restored $($changes.Count) files. Learning records and runtime were not changed."
