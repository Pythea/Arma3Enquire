# Arma3Enquire
Arma3Enquire is a Linux CLI mod manager for Arma 3 written in Python

Installation:

Linux Package Requirements:
  screen
  steamCMD

Python Package Requirements:
  beautifulsoup4, 
  enquiries

This program assumes that you have a working Arma 3 Linux server. If you don't there are instructions <a href="https://community.bistudio.com/wiki/Arma_3:_Dedicated_Server">here</a> to set one up

When first running the program with it is important to configure it to your setup. In order to do so there is a menu called Enquire Options which contains:

* The location for your arma 3 install directory
* The steam account used by steamcmd to download workshop mods
* A steam workshop collection ID to download your mods from
* The location for your server start script
 
Note: This program currently only supports downloading mods from a steam collection, so one is required for this program to work at the moment.
