#!/usr/bin/env bash

echo "Setting up Environment"
echo "###### Updating apt-get #############"
sudo apt-get update
echo "###### Done #########################"
echo "###### Installing python-pip ########"
sudo apt-get install -y python-pip
echo "###### Done #########################"
echo "###### Installing Kazoo module ######"
pip install kazoo
echo "###### Done #########################"
echo "###### Installing NumPy module ######"
pip install numpy
echo "###### Done #########################"
cp watcher.py watcher
cp player.py player
