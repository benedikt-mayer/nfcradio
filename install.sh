red=`tput setaf 1`
reset=`tput sgr0`
# edit config file
tput setaf 2;echo "------------------------------------------------"
echo "writing i2c information to /etc/modules"
echo "------------------------------------------------"
tput sgr0

if ! grep -q "i2c-bcm2708" /etc/modules
then
    echo "i2c-bcm2708" >> /etc/modules
else 
    echo "i2c data already added"
fi

# add soundcard
tput setaf 2;echo "------------------------------------------------"
echo "making the usb soundcard the default"
echo "------------------------------------------------"
tput sgr0

if ! grep -Pzoq "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" /etc/asound.conf
then
    touch /etc/asound.conf
    echo "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" >> /etc/asound.conf
    amixer set PCM 80%
else 
    echo "soundcard configuration data already added"
fi

# update all installed packages just in case
tput setaf 2;echo "------------------------------------------------"
echo "updating all installed packages"
echo "------------------------------------------------"
tput sgr0

sudo apt-get update
sudo apt-get upgrade

# pip
tput setaf 2;echo "------------------------------------------------"
echo "installing pip"
echo "------------------------------------------------"
tput sgr0

sudo apt install python-pip

# display libraries
tput setaf 2;echo "------------------------------------------------"
echo "installing python dependencies"
echo "------------------------------------------------"
tput sgr0

sudo apt-get install python-dev
sudo apt-get install python-smbus
sudo apt-get install python-serial
sudo apt-get install python-imaging

# install spi-dev
tput setaf 2;echo "------------------------------------------------"
echo "installing spi-dev"
echo "------------------------------------------------"
tput sgr0;

$currentdir = echo pwd
cd ~
mkdir python-spi
cd python-spi
wget https://raw.github.com/doceme/py-spidev/master/setup.py
wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
wget https://raw.github.com/doceme/py-spidev/master/README.md
wget https://raw.github.com/doceme/py-spidev/master/CHANGELOG.md
sudo python setup.py install
cd $currentdir

# python libraries
tput setaf 2;echo "------------------------------------------------"
echo "installing python libraries"
echo "------------------------------------------------"
tput sgr0;

pip install Pillow
pip install pygame

# add our scripts to autostart
tput setaf 2;echo "------------------------------------------------"
echo "adding scripts to autostart"
echo "------------------------------------------------"
tput sgr0;

run_autostart_script()
{
    ANSWER=$1
    if "$ANSWER" = "master"
    then
        # if there is no such line already, add it
        if ! grep -q "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Master/MasterMain.py" /home/pi/.config/lxsession/LXDE-pi/autostart
        then
            echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Master/MasterMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
        else 
            echo "autostart data already added"
        fi
    elif "$ANSWER" = "slave"
    then
        # if there is no such line already, add it
        if ! grep -q "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Slave/SlaveMain.py" /home/pi/.config/lxsession/LXDE-pi/autostart
        then
            echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Slave/SlaveMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
        else 
            echo "autostart data already added"
        fi
    else 
        echo "wrong input! are you running on the ${red}master${reset} or ${red}slave${reset}?"
        read alternative_user_input
        run_autostart_script $alternative_user_input
    fi
}
echo "setting up autostart. are you running on the ${red}master${reset} or ${red}slave${reset}?"
read user_input
run_autostart_script $user_input

# completed
tput setaf 2;echo "------------------------------------------------"
echo "done"
echo "------------------------------------------------"

# now reboot
reboot_prompt()
{
    if $1 = "yes"
    then
        echo "${red}rebooting in 5 seconds."
        sleep 1
        echo "rebooting in 4 seconds."
        sleep 1
        echo "rebooting in 3 seconds."
        sleep 1
        echo "rebooting in 2 seconds."
        sleep 1
        echo "rebooting in 1 seconds.${reset}"
        sleep 1
        reboot
    elif $1 = "no"
        echo "not rebooting. not all changes will take effect."
    else
        echo "wrong input! a reboot is necessary for the changes to change effect. do you want to reboot now? ${red}yes${reset} or ${red}no${reset}?"
        read reboot_input
        reboot_prompt $reboot_input
    fi
}
echo "a reboot is necessary for the changes to change effect. do you want to reboot now? ${red}yes${reset} or ${red}no${reset}?"
read reboot_input
reboot_prompt $reboot_input