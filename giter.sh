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
		# if [ ! -f "$dir/.history_changes" ]; then
		# 	echo "[!] '.history_changes' not found in $dir. Consider execute giter -p(pull) or -f(fetch) to obtain last changes data."
		# 	datetime=$(date | awk '{NF=""}1')
		# 	echo -e "$datetime -> add: '.history_changes to .gitignore (not commited)" > $dir/.history_changes
		# 	echo ".history_changes" >> $dir/.gitignore
		# fi
	fi
done

# Obtain Git Data
for repo in ${validDirs[@]}; do
	gitCount=$(git -C $repo status -s | wc -l)
	# lastChanges=$(cat $repo/.history_changes | tail -1)
	# echo -e "Last changes: $lastChanges"
	if [ "$repo" == "." ]; then
		echo -e "${purple}[*] Directory: ${end}${gray}${repo/./$(basename "$PWD")}${end} (current dir)"
	else
		if [ $gitCount -gt 0 ]; then
			echo -e "${turquoise}[*] Directory: ${end}${gray}$repo${end}"
		else
			echo -e "${blue}[*] Directory: ${end}${gray}$repo${end} (no changes)"
		fi
	fi
	if [ $gitCount -gt 0 ]; then
		git -C $repo status -s
	fi
	commitId=$(git -C $repo log --oneline | head -n1 | awk ' { print $1 } ')
	commitDesc=$(git -C $repo log --oneline | head -n1 | cut -d\  -f2- )
	echo -e "($commitId) '$commitDesc'"
	echo ""
done
