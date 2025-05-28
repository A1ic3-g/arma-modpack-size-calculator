#!/bin/bash

get_size_bytes() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        du -sb "$dir" 2>/dev/null | cut -f1
    else
        echo 0
    fi
}

# Prompt for modpack HTML
while true; do
    read -rp "Enter path to modpack .html file: " modpack_path
    modpack_path="${modpack_path/#\~/$HOME}"  # expand ~ manually
    if [[ -f "$modpack_path" ]]; then
        break
    else
        echo "File not found, please try again."
    fi
done

# Prompt for workshop path
while true; do
    read -rp "Enter Arma 3 workshop folder path (e.g. ~/Steam/steamapps/workshop/content/107410): " workshop_path
    workshop_path="${workshop_path/#\~/$HOME}"  # expand ~ manually
    if [[ -d "$workshop_path" ]]; then
        break
    else
        echo "Directory not found, please try again."
    fi
done

# Check for xmlstarlet
if ! command -v xmlstarlet &>/dev/null; then
    echo "This script requires 'xmlstarlet'. Please install it first (e.g., sudo apt install xmlstarlet)."
    exit 1
fi

# Temporary file to store results
tempfile=./tmp #$(mktemp)
total_bytes=0

# Extract mod names and hrefs, then process
mapfile -t lines < <(xmlstarlet sel -t -m '//tr[@data-type="ModContainer"]' \
    -v 'td[@data-type="DisplayName"]' -o $'\t' \
    -v 'td/a/@href' -n "$modpack_path")

for line in "${lines[@]}"; do
    IFS=$'\t' read -r name href <<< "$line"
    id=$(echo "$href" | grep -oP 'id=\K\d+')
    if [[ -n "$id" ]]; then
        path="$workshop_path/$id"
        size_bytes=$(get_size_bytes "$path")
        total_bytes=$((total_bytes + size_bytes))
        size_mb=$(awk -v b="$size_bytes" 'BEGIN { printf "%.2f", b / (1024*1024) }')
        echo -e "${id}\t${name}\t${size_mb}" >> "$tempfile"
    fi
done

# Print table
printf "%-12s %-45s %10s\n" "ID" "Name" "Size (MB)"
sort -t $'\t' -k3,3n "$tempfile" |
while IFS=$'\t' read -r id name size; do
    printf "%-12s %-45s %10s\n" "$id" "$name" "$size"
done

rm "$tempfile"

# Print total size in GB
total_gb=$(awk -v b="$total_bytes" 'BEGIN { printf "%.2f", b / (1024*1024*1024) }')
echo
echo "Total size: $total_gb GB"