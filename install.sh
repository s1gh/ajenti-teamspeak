#!/bin/bash

########################################
# First install the python-ts3 library #
########################################
# Download the newest version of python-ts3
wget https://github.com/nikdoof/python-ts3/archive/develop.zip

# Unzip the package
unzip develop.zip && rm develop.zip

# Change directory
cd python-ts3-develop

# Install python-ts3 library
python setup.py install

# Change directory (back)
cd ..

# Remove the python-ts3-develop folder
sudo rm -rf python-ts3-develop

######################################## 
#      Install the Ajenti Plugin       #
########################################
# Create the plugin directory
mkdir /var/lib/ajenti/plugins/teamspeak3

# Copy all python files and the layout folder
cp -r *.py layout /var/lib/ajenti/plugins/teamspeak3

########################################
#      Restart the Ajenti Service      #
#     (Uncomment the one you need)     #
########################################
# Arch Linux
#systemctl restart ajenti

# Ubuntu
#service ajenti restart