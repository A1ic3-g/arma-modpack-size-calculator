#!/bin/bash

ID_START="?id="

get_size_bytes() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        du -sb "$dir" 2>/dev/null | awk '{print $1}'
    else
        echo 0
    fi
}

# Prompt for modpack HTML
while true; do
    read -rp "Enter path to modpack .html file: " modpack_path
    if [[ -f "$modpack_path" ]]; then
        break
    else
        echo "File not found, please try again."
    fi
done

# Extract mod names and IDs
mapfile -t mods < <(grep -A2 'data-type="DisplayName"' "$modpack_path" | \
    paste - - - | \
    sed -E 's|.*data-type="DisplayName">([^<]+).*filedetails/\?id=([0-9]+).*|\2\t\1|')

# Prompt for workshop folder
while true; do
    read -rp "Enter Arma 3 workshop folder path (e.g. ~/Steam/steamapps/workshop/content/107410): " workshop_path
    if [[ -d "$workshop_path" && "$workshop_path" != *"!WORKSHOP"* ]]; then
        break
    else
        echo "Invalid folder. Please make sure you're entering the actual Steam workshop content folder, not !WORKSHOP."
    fi
done

# Process each mod
printf "ID\tName\tSize (MB)\n"
total_size=0
for line in "${mods[@]}"; do
    mod_id=$(echo "$line" | cut -f1)
    mod_name=$(echo "$line" | cut -f2)
    mod_dir="${workshop_path}/${mod_id}"
    size_bytes=$(get_size_bytes "$mod_dir")
    size_mb=$(awk -v s="$size_bytes" 'BEGIN { printf "%.2f", s / (1024 * 1024) }')
    total_size=$((total_size + size_bytes))
    printf "%s\t%s\t%s\n" "$mod_id" "$mod_name" "$size_mb"
done | sort -k3 -nr

# Total summary
echo
echo "Traditional 1024 scale (used by Windows): $((total_size / 1024 / 1024)) MB"
echo "SI 1000 scale: $((total_size / 1000 / 1000)) MB"
