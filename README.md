# arcolinux-netinstall-explorer
Export list of packages from Calamares netinstall yaml files

```python
python netinstall-explorer.py --help
usage: Calamares netinstall package explorer [-h] [--config CONFIG]

Output a list of packages from Calamares netinstall YAML files

options:
  -h, --help       show this help message and exit
  --config CONFIG  Choose from: arcopro-calamares-config, arconet-calamares-config, arcoplasma-calamares-config
  --find FIND      Find package name
```
## Generate list of packages

```sh
./netinstall-explorer.py --config arconet-calamares-config

Category = netinstall-applications | Packages = 46
Category = netinstall-arcolinux | Packages = 90
Category = netinstall-arcolinuxdev | Packages = 16
Category = netinstall-communication | Packages = 29
Category = netinstall-desktop-wayland | Packages = 50
Category = netinstall-desktop | Packages = 205
Category = netinstall-development | Packages = 27
Category = netinstall-drivers | Packages = 6
Category = netinstall-filemanagers | Packages = 16
Category = netinstall-fonts | Packages = 47
Category = netinstall-gaming | Packages = 50
Category = netinstall-graphics | Packages = 6
Category = netinstall-internet | Packages = 41
Category = netinstall-kernel | Packages = 12
Category = netinstall-login | Packages = 15
Category = netinstall-multimedia | Packages = 61
Category = netinstall-nvidia | Packages = 43
Category = netinstall-office | Packages = 26
Category = netinstall-terminals | Packages = 72
Category = netinstall-theming | Packages = 111
Category = netinstall-usb | Packages = 15
Category = netinstall-utilities | Packages = 139
Packages total = 1123
```

A text file is generated inside `$HOME/arcolinux-netinstall-explorer`

Truncated output.

```text
####### arconet-calamares-config package log #######
####### NETINSTALL-APPLICATIONS (46) #######
 - cheese
 - font-manager
 - galculator
 - gpick
 - flameshot-git
 - liferea
 - mediainfo-gui
 - mcomix
 - nitrogen
 - nomacs
 - nomacs-git
 - nomacs-qt6-git
 - pdfarranger
 - plank
 - arcolinux-plank-themes-git
 - screenkey-git
 - variety
 - arcolinux-conky-collection-git
 - arcolinux-pipemenus-git
 - conky-lua-archers
 ....
 ```
## Finding a package

```sh
./netinstall-explorer.py --config arconet-calamares-config --find firefox
############# Search results (3) #############
 - Package = firefox | Caregory = netinstall-internet
 - Package = firefox-adblock-plus | Caregory = netinstall-internet
 - Package = firefox-ublock-origin | Caregory = netinstall-internet
```