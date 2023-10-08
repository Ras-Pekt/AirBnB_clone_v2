#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

# installing nginx if it doesn't exist
if ! command -v nginx &>/dev/null
then
	sudo apt-get update
	sudo apt-get install nginx -y
fi

# creating folders if they do not exist
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# creating file to test nginx
sudo touch /data/web_static/releases/test/index.html
echo "Hello Friend!" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# deleting and recreating a symlink
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# giving ownership to /data/ folder
sudo chown -R ubuntu:ubuntu /data/

# updating the Nginx configuration
old_block="server_name _;"
new_block="server_name _;\n\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web\_static\/current\/;\n\t}"
sudo sed -i "s/$old_block/$new_block/" /etc/nginx/sites-available/default

# restarting nginx
sudo service nginx restart
