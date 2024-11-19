#!/bin/zsh

if [ -z $0 ]; then
	version=$(cat /home/$user/Desktop/Discord/.version)
else
	version=$0
fi
user=$(id -un)
curl -s -X GET "https://stable.dl2.discordapp.net/apps/linux/0.0.${version}/discord-0.0.${version}.tar.gz" -o /home/$user/Desktop/discord.tar.gz
gzip /home/$user/Desktop/discord.tar.gz -d
tar -xf /home/$user/Desktop/discord.tar -C /home/$user/Desktop/
chmod +x /home/$user/Desktop/Discord/Discord
rm /home/$user/Desktop/discord.tar
echo $(($version+1)) > /home/$user/Desktop/Discord/.version
/home/$user/Desktop/Discord/Discord
