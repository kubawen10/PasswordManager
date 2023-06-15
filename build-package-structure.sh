#!/bin/bash

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






