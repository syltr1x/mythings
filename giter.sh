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


help_menu() {
	echo "AYUDA\nMENU"
}

obtain_dirs() {
	if [ $# -eq 1 ]; then
		files_list=$(find . $1 -type d)
	else
		files_list=$(find . -type d)
	fi
	# Directory List
	while IFS= read -r linea; do
		firstChar=${linea:0:1}
		linea=$(awk '{print $NF}' <<< "$linea")
		if [ "$linea" != "." ] && [ "$linea" != ".." ]; then
			dirList+=("$linea")
		fi
	done <<< "$files_list"

	# Directory Scan
	for dir in ${dirList[@]}; do
		if [ -d "$dir/.git" ]; then
			validDirs+=("$dir")
		fi
	done
	echo ${validDirs[@]}
}
giter() {
	validDirs=$(obtain_dirs $dirParams)
	giter $hidden $recursive $pull $fetch
	if [ ! $recursive ]; then
		dirParams="-maxdepth 1"
	fi
	if [ $pull ]; then
		gitComm="pull"
	elif [ $fetch ]; then	
		gitComm="fetch"
	else
		gitComm="status -s"
	fi
	# Obtain Git Data
	for repo in ${validDirs[@]}; do
		gitCount=$(git -C $repo status -s | wc -l)
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
			git -C $repo $gitComm
		fi
		commitId=$(git -C $repo log --oneline | head -n1 | awk ' { print $1 } ')
		commitDesc=$(git -C $repo log --oneline | head -n1 | cut -d\  -f2- )
		echo -e "($commitId) '$commitDesc'"
		echo ""
	done
}

# Initial Variables
display_help=false
hidden=false
recursive=false
pull=false
fetch=false

# Parameters
while getopts ":h :a :r :p :pr :f :fr" arg; do
	case $arg in
		h) display_help=true;;
		a) hidden=true;; 
		r) recursive=true;;
		p) pull=true;;
		f) fetch=true;;
	esac
done
echo $display_help
# if [ $display_help == true ]; then
# 	help_menu
# else
# 	giter $hidden $recursive $pull $fetch
# fi
