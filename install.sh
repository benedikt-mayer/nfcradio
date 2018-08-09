# edit config file
if ! grep -q "i2c-bcm2708" /etc/modules
then
    echo "i2c-bcm2708" >> /etc/modules
else 
    echo "i2c data already added"
fi
# update apt-get just in case
sudo apt-get update
# pip
sudo apt install python-pip
# display libraries
sudo apt-get install python-dev
sudo apt-get install python-smbus
sudo apt-get install python-serial
sudo apt-get install python-imaging
sudo apt-get install pcregrep
# install spi-dev
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
pip install Pillow
pip install pygame
# add soundcard
if ! grep -Pzoq "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" /etc/asound.conf
then
    touch /etc/asound.conf
    echo "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" >> /etc/asound.conf
    amixer set PCM 80%
else 
    echo "soundcard configuration data already added"
fi
# add our scripts to autostart
run_autostart_script()
{
    ANSWER=$1
    if [ "$ANSWER" = "master" ]
    then
        # if there is no such line already, add it
        if ! grep -q "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Master/MasterMain.py" /home/pi/.config/lxsession/LXDE-pi/autostart
        then
            echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Master/MasterMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
        else 
            echo "autostart data already added"
        fi
    elif [ "$ANSWER" = "slave" ]
    then
        # if there is no such line already, add it
        if ! grep -q "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Slave/SlaveMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
        then
            echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Slave/SlaveMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
        else 
            echo "autostart data already added"
        fi
    else 
        echo "wrong input! please write master or slave"
        read user_input
        run_autostart_script $user_input
    fi
}
echo "setting up autostart. Are you running on the master or slave?"
read user_input
run_autostart_script $user_input