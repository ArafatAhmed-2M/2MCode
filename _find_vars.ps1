$root = "c:\Users\pc\Desktop\2M Code"
$files = Get-ChildItem -Path $root -Recurse -Include *.ts,*.tsx -Exclude *.d.ts -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "node_modules" -and $_.FullName -notmatch "\.git" }

$matches = @{}
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $results = [regex]::Matches($content, '\b2M_CODE_[A-Z_]+\b')
    foreach ($match in $results) {
        $matches[$match.Value] = $true
    }
}
$matches.Keys | Sort-Object
