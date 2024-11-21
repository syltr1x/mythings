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
	echo "-h: Display this help panel"
	echo "-a: Inlcude hidden folders/repos"
	echo "-r: Recursive folder search"
	echo "-p: make pull in each repo"
	echo "-f: make fetch in each repo"
	echo "-u: update giter"
}

update_giter() {
	echo "[*] Downloading file..."
	curl -s https://raw.githubusercontent.com/syltr1x/mythings/main/giter.sh -o $(which giter)
	if [ $? -eq 0 ]; then
		echo -e "${green}[+] ${end}File downloaded"
		sudo chmod +x $(which giter)
	else
		echo -e "${red}[-] ${end}Error in donwload"
	fi
}

obtain_dirs() {
	params=${@:-""}
	# Directory List
	while IFS= read -r linea; do
		firstChar=${linea:0:1}
		linea=$(awk '{print $NF}' <<< "$linea")
		if [ "$linea" != "." ] && [ "$linea" != ".." ]; then
			dirList+=("$linea")
		fi
	done < <(find . $params -type d)

	# Directory Scan
	for dir in ${dirList[@]}; do
		if [ -d "$dir/.git" ]; then
			validDirs+=("$dir")
		fi
	done
	echo ${validDirs[@]}
}
giter() {
	# $hidden $recursive $pull $fetch (Parameters order 1..4)
	if [ $2 == "false" ]; then
		dirParams="-maxdepth 1"
	fi
	validDirs=$(obtain_dirs $dirParams)
	if [ $3 != "false" ]; then
		gitComm="pull"
	elif [ $4 != "false" ]; then	
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
		branch=$(git -C $repo symbolic-ref --short HEAD)
		commitId=$(git -C $repo log --oneline -1 origin/$branch | awk ' { print $1 } ')
		commitDesc=$(git -C $repo log --oneline -1 origin/$branch | cut -d\  -f2- )
		echo -e "${green}Remote HEAD: ${end}${yellow}($commitId)${end} '$commitDesc'"
		commitId=$(git -C $repo log --oneline origin/$branch..HEAD | awk ' { print $1 } ')
		commitDesc=$(git -C $repo log --oneline origin/$branch..HEAD | cut -d\  -f2- )
		if [[ ! -z $commitId ]]; then
			echo -e "${red}Local HEAD: ${end}${yellow}($commitId)${end} '$commitDesc'"
		fi
	done
}

# Initial Variables
display_help=false
update=false
hidden=false
recursive=false
pull=false
fetch=false

# Parameters
while getopts ":h :a :r :p :f :u" arg; do
	case $arg in
		h) display_help=true;;
		a) hidden=true;; 
		r) recursive=true;;
		p) pull=true;;
		f) fetch=true;;
		u) update=true;;
	esac
done

if [ $display_help == true ]; then
	help_menu
elif [ $update == true ]; then
	update_giter
else
	giter $hidden $recursive $pull $fetch
fi
