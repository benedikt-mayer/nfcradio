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