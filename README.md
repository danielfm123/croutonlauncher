#Crouton Launcher
##Run Crouton apps as normal ChromeOS windows

#Install :
1. Get the dependencies :
```
sudo apt-get install python3 python3-xdg git
```
2. Download the Software on chroot /opt
```
git clone https://github.com/danielfm123/croutonlauncher.git
sudo chmof 777 /opt/croutonlauncher
cd croutonlauncher
rm index.html
```
3. Make a Systemlink (This is because the python web server needs to be able to serve content above the directory it is running in, this is not obligatory but you will not see icons if you do not create the link)
```
ln -s / system
```
4. Install the Chrome Extention provided in the repo by dragging to extensions menu in chrome, dots/more tools/extensions (remember to check developer mode)

5. Now you can launch executing main.py

6. open localhost:8000 or launche the chrome extension.
i recomend to place the extension pined on the menu and configure as not a tab.

# autostart 
(adapted from https://github.com/dnschneid/crouton/wiki/Autostart-crouton-chroot-at-ChromeOS-startup)
1. from chroot copy /opt/croutonlauncher/autostart to ~/Downloads
```
cp -r /opt/croutonlauncher/autostart ~/Downloads
```
2. open a shell (outside chroot)
3. make / writable
```
sudo  ~/Downloads/rw-rootfs
```
4. configure ~/Downloads/local/crouton.init
this file contains the configurations
modify line 33 writing the name of your chroot, default is bionic, might be xenial too

5. place files on system folders
```
sudo cp ~/Downloads/local/crouton.init /usr/local
sudo cp ~/Downloads/init/crouton.conf /etc/init
sudo cp ~/Downloads/init/mnt-crouton.conf /etc/init
```

6. restart and proffit
