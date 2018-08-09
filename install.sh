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
# Display libraries
sudo apt-get install python-dev
sudo apt-get install python-smbus
sudo apt-get install python-serial
sudo apt-get install python-imaging
# insert installspidev.sh here
# python libraries
pip install Pillow
# pip install Image
# pip install ImageDraw
# pip install ImageFont
pip install pygame
# maybe add card 1 etc. to asound.conf