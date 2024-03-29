#!/bin/sh
opt=()
while IFS= read -r line; do
    opt+=("$(basename "$line")")
done < <(find / -perm -4000 2>/dev/null)

while IFS= read -r line; do
	filter=$(echo "$line" | cut -d ' ' -f 1)
    line=$(echo "$line" | sed 's/[[:space:]]*$//')
    for elemento in "${opt[@]}"; do
		if [[ "$elemento" == "$filter" ]]; then
            echo "$line"
		fi
    done
done < suid
