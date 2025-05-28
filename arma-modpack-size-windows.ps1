function Get-FolderSize {
    param (
        [string]$Path
    )

    $size = 0
    if (Test-Path $Path) {
        Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $size += $_.Length
        }
    }
    return $size
}

# Prompt for modpack HTML file
do {
    $modpack_path = Read-Host "Enter path to modpack .html file"
    $modpack_found = Test-Path $modpack_path
    if (-not $modpack_found) {
        Write-Host "File not found, please try again." -ForegroundColor Red
    }
} until ($modpack_found)

# Load HTML and parse it
[xml]$htmlDoc = Get-Content -Path $modpack_path -Raw
$rows = $htmlDoc.getElementsByTagName("tr")

# Create list of objects to store mod info
$modpack = @()
$ID_START = '?id='

foreach ($mod in $rows) {
    $modNameNode = $mod.getElementsByTagName("td") | Where-Object { $_.getAttribute("data-type") -eq "DisplayName" }
    if ($modNameNode) {
        $modName = $modNameNode.InnerText.Trim()
        $link = $mod.getElementsByTagName("a") | Select-Object -First 1
        if ($link) {
            $href = $link.getAttribute("href")
            $idIndex = $href.IndexOf($ID_START)
            if ($idIndex -ge 0) {
                $id = $href.Substring($idIndex + $ID_START.Length)
                $modpack += [PSCustomObject]@{
                    ID   = $id
                    Name = $modName
                    Size = 0
                }
            }
        }
    }
}

# Prompt for valid workshop folder
do {
    $workshop_folder_path = Read-Host "Enter workshop folder path"
    $validPath = (Test-Path $workshop_folder_path) -and ($workshop_folder_path -notmatch "!WORKSHOP")
    if (-not $validPath) {
        Write-Host "Invalid folder path. Ensure you're NOT entering your !WORKSHOP folder." -ForegroundColor Red
        Write-Host "A typical workshop folder path looks like steamapps\workshop\content\107410"
    }
} until ($validPath)

# Calculate folder sizes
$totalSize = 0
for ($i = 0; $i -lt $modpack.Count; $i++) {
    $mod = $modpack[$i]
    $modPath = Join-Path -Path $workshop_folder_path -ChildPath $mod.ID
    $sizeBytes = Get-FolderSize -Path $modPath
    $modpack[$i].Size = $sizeBytes
    $totalSize += $sizeBytes
}

# Sort and display table
$modpack |
    Sort-Object Size |
    Select-Object ID, Name, @{Name="Size (MB)"; Expression={[math]::Round($_.Size / 1MB, 2)}} |
    Format-Table -AutoSize

# Display total sizes

$totalGb = [math]::Round($totalSize / 1GB, 2)

Write-Host "`nTotal Size: $totalGb GB"

Read-Host -Prompt "Press Enter to exit"
