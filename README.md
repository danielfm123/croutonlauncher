#Crouton Launcher
##Run Crouton apps as normal ChromeOS windows

#Install :
1. Get the dependencies :
```
sudo apt-get install python3 python3-xdg git
```
2. Download the Software
```
git clone https://github.com/jmaris/croutonlauncher.git
cd croutonlauncher
```
3. Make a Systemlink (This is because the python web server needs to be able to serve content above the directory it is running in, this is not obligatory but you will not see icons if you do not create the link)
```
ln -s / system
```
4. run ./main.py
5. Install the Chrome Extention provided in the repo
6. Be sure to have already installed the crouton extension for chromeos and the xiwi and extension targets in your chroot.
7. Pin the chrome extention on your shelf.
8. Have Fun.

edit crlauncher and place on /usr/local/bin
