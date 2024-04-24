#!/bin/sh

# Variables
dirList=()
params=()

# Parameters
for i in "$@"; do
	if [ $i == '-h' ]; then
		params+=(" -a")
	fi
done

# Directory List
while IFS= read -r linea; do
	firstChar=${linea:0:1}
	if [ "$firstChar" == "d" ]; then
		linea=$(awk '{print $NF}' <<< "$linea")
		if [ "$linea" != "." ] && [ "$linea" != ".." ]; then
			dirList+=("$linea")
		fi
	fi
done < <(ls -l ${params[@]})

# Directory Scan
for dir in ${dirList[@]}; do
	if [ ! -d "$dir/.git" ]; then
		dirList=("${dirList[@]/$dir}")
	fi
done

# Obtain Git Data
for repo in ${dirList[@]}; do
	gitData=$(git -C $repo status -s)
	gitCount=$(wc -l <<< $gitData)
	if [ $gitCount -gt 1 ]; then
		echo "==========$repo=========="
		echo "$gitData"
		echo ""
	fi
done
