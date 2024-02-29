#!/bin/sh
user=$(grep -E '/bin/[^/]sh' /etc/passwd | grep -v '^root:' | awk -F: '{ print $1}')
cd ~
git clone https://aur.archlinux.org/spotify.git
cd spotify
makepkg -si
chmod +x spotify.sh
./spotify.sh
chmod a+rw /opt/spotify/Apps
chmod a+rw /opt/spotify/Apps/*
sudo chown -R $user:$user /opt/spotify
curl -fsSL https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.sh | sh
echo "Ya puedes modificar como quiera su spotify"
