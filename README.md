#Crouton Launcher
##Run Crouton apps as normal ChromeOS windows

#Install :
1. Get the dependencies :
```
sudo apt-get install python3 python3-xdg git
```
2. Download the Software
```
git clone https://github.com/danielfm123/croutonlauncher.git
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
9. edit crlauncher and place on /usr/local/bin on the chrome root, not chroot


if you want autostart follow this instrucions from https://www.maketecheasier.com/autostart-crouton-chromeos/
and set as DE enter-chroot
as command line on boot the path to the launcher
