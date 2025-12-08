#!/bin/bash

echo "========================================="
echo "Nginx Installation Script"
echo "========================================="

nginx -v &>/dev/null

exit_code=$?
if [ $exit_code -eq 0 ]; then
     echo "Nginx is already installed"
else
    sudo apt update
    sudo apt install nginx -y
    echo "Nginx is done installing and ready to use"
fi