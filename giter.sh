#!/bin/bash

# Colours
green="\e[0;32m\033[1m"
end="\033[0m\e[0m"
red="\e[0;31m\033[1m"
blue="\e[0;34m\033[1m"
yellow="\e[0;33m\033[1m"
purple="\e[0;35m\033[1m"
turquoise="\e[0;36m\033[1m"
gray="\e[0;37m\033[1m"

# Variables
dirList=(".")
validDirs=()
params=("-maxdepth 1")

# Parameters
while getopts ":h :r" arg; do
	case $arg in
		h) params+=("-maxdepth 1");;
		r) params=("");;
	esac
done

# Directory List
while IFS= read -r linea; do
	firstChar=${linea:0:1}
	linea=$(awk '{print $NF}' <<< "$linea")
	if [ "$linea" != "." ] && [ "$linea" != ".." ]; then
		dirList+=("$linea")
	fi
done < <(find . ${params[@]} -type d)

# Directory Scan
for dir in ${dirList[@]}; do
	if [ -d "$dir/.git" ]; then
		validDirs+=("$dir")
	fi
done

# Obtain Git Data
for repo in ${validDirs[@]}; do
	gitCount=$(git -C $repo status -s | wc -l)
	if [ $gitCount -gt 0 ]; then
		if [ "$repo" == "." ]; then
			echo -e "${purple}[*] Directory: ${end}${gray}./${repo/./$(basename "$PWD")}${end} (current dir)"
		else
			echo -e "${turquoise}[*] Directory: ${end}${gray}$repo${end}"
		fi
		git -C $repo status -s
		echo ""
	else
		echo -e "${blue}[*] Directory: ${end}${gray}$repo${end} (no changes)"
	fi
done
