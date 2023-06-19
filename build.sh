#! /bin/bash

# create venv and install requirements
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install ruby
sudo apt update
sudo apt install ruby3.0.0
gem install fpm --user-install
export PATH="/home/`whoami`/.local/share/gem/ruby/3.0.0/bin:$PATH"

# create exe 
pyinstaller password-manager.spec

# Create folders
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# Copy files
cp -r dist/PasswordManager package/opt/PasswordManager
cp src/uis/icons/lock.svg package/usr/share/icons/hicolor/scalable/apps/password-manager-lock.svg
cp password-manager.desktop package/usr/share/applications

# Change permissions
find package/opt/PasswordManager -type f -exec chmod 644 -- {} +
find package/opt/PasswordManager -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/PasswordManager/PasswordManager

# build package
fpm

# install package
sudo dpkg -i password-manager.deb

