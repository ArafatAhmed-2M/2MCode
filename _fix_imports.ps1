$root = "c:\Users\pc\Desktop\2M Code"
$files = Get-ChildItem -Path $root -Recurse -Include *.ts,*.tsx -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "node_modules" -and $_.FullName -notmatch "\.git" }

$count = 0
foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $newContent = $content -replace '@2M_CODE-ai', '@2mcode-ai'
        
        if ($newContent -ne $content) {
            [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
            $count++
            Write-Host "Fixed $($file.Name)"
        }
    } catch { }
}
Write-Host "Fixed $count ts/tsx files"
