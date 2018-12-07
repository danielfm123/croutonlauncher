# [Video of the result](https://www.youtube.com/watch?v=z-rkn5SXD4k)

# Requirements

Having the chromebook in developer mode and crouton executable on Downloads folder https://github.com/dnschneid/crouton

I installed with: sudo sh ~/Downloads/crouton -t xiwi,extension,keyboard,cli-extra -r bionic

# Crouton Launcher

fork from https://github.com/jmaris/croutonlauncher

## Run Crouton apps as normal ChromeOS tabs on boot

This was tested using crouton installed with this commands:
open a terminal with ctrl + alt + t
```
shell
sudo sh ~/Downloads/crouton -t xiwi,keyboard,extension,cli-extra,audio -r bionic
```

## Install Menu:

0.enter to the chroot
```
sudo enter-chroot
```

1. Get the dependencies:
```
sudo apt-get install python3 python3-xdg git
```
2. Download the Software on chroot /opt
```
sudo chmod 777 /opt
cd /opt
git clone https://github.com/danielfm123/croutonlauncher.git
sudo chmod 755 /opt/croutonlauncher
```
3. Install the Chrome Extention provided in the repo by dragging to extensions menu in chrome, dots/more tools/extensions (remember to check developer mode)

4. Now you can launch executing main.py
```
/opt/croutonlauncher/main.py
```

6. Open with chrome http://localhost:8000 , the menu should be visible as a website.

7. Instal the extension
First put it in the downloads folder with the command:
```
cp /opt/croutonlauncher/CroutonLauncher-Chrome.crx  ~/Downloads/
```
Then 3 drots menu - more tools - extensions , check developer mode is turned on and drag the crx file from Downloads the the extesions menu.

I Recomend to place the extension pinned to the menu and configure as not a tab.

If you just want to launch the server from shell and not autostart the menu,the command to launch from shell would be
```
sudo enter-chroot /opt/croutonlauncher/main.py
```

# Autostart on boot
 
adapted from https://github.com/dnschneid/crouton/wiki/Autostart-crouton-chroot-at-ChromeOS-startup

1. from chroot copy /opt/croutonlauncher/autostart to ~/Downloads
```
cp -r /opt/croutonlauncher/autostart ~/Downloads
```
2. open a shell (outside chroot)
press ctrl + alt + t then open a shell (not a crosh)
```
shell
```

3. make root fs writable
```
sudo sh ~/Downloads/autostart/rw-rootfs
```
restart the chromebook

4. edit ~/Downloads/local/crouton.init on line 33 to put you chroot name
default is bionic, might be xenial too

5. place files on system folders
```
sudo cp ~/Downloads/autostart/local/crouton.init /usr/local
sudo cp ~/Downloads/autostart/init/crouton.conf /etc/init
sudo cp ~/Downloads/autostart/init/mnt-crouton.conf /etc/init
```
Now you can delete Downloads/autostart

6. restart and profit from http://localhost:8000 or crouton extension
