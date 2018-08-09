# Software Installation Instructions
1. Arduino software
    1. Create an account on [Arduino Create](https://create.arduino.cc/).
    2. Install the Arduino Create plugin from [here](https://create.arduino.cc/getting-started/plugin).
    3. Retrieve your nfc tag UID
        1. Now load the sketch `read_nfc_tag` to the arduino while connected to your computer.
        2. Approximate your nfc tag / card to the nfc reader.
        3. Look at the Monitor on the left of the editor for a UID: it looks like this `CE 2F F1 D9`, but can be shorter or longer
    4. Now that you have your UID, modify the sketch `read_rfid_potentiometer`
        1. Replace the UIDs in line 115 and 122 with your UIDs. One is enough, two are better so that you can change albums / genres.
        2. Save and upload the script to the Arduino.
        3. Now connect the Arduino to your Master Raspberry Pi and reboot the Pi.
2. Raspberry software
    1. Get "Raspbian Stretch with Desktop" from and follow instructions on https://www.raspberrypi.org/downloads/raspbian/.
    2. To set up some options, open a terminal and run `sudo raspi-config`:
        1. In the settings, select **Interfacing Options** -> **I2C** -> **Yes**, to start up the I2C core driver.
        2. Go to **Network Options** -> **Wi-fi**, now enter the **SSID** and **password** of your access point / router. Now you have a internet connection to install software!
        3. The serial port of RPi is set to serial terminal debugging function mode by default. If you want the serial port services as a common IO, you should modify the settings on the RPi.  
        Go to **Interfacing Options** -> **Serial** and select **No** in the first and **Yes** in the second dialog.
    3. Then you also need to modify the configuration file. Run the following command to open the configuration file: `sudo nano /etc/modules`.
        1. Add the following two lines to the configuration file:  
           `i2c-bcm2708`  
           Press the keys Ctrl+X to exit, and input Y to save the settings. Then, reboot the module to make the settings take effect.
    4. When logged into the Raspberries, pull the source code from [Github](https://github.com/benedikt-mayer/nfcradio).
    5. Run the shell script in the root repository of the git folder by opening a terminal and running `sudo sh install.sh` to install all necessary python libraries.
    6. Manually run the scripts to see if everything was installed properly:
        1. Navigate to the slave / master folder in PEM2/project/src/Slave / PEM2/project/src/Master 
        2. Manually run the Slave and Master scripts by calling `sudo python MasterMain.python` and `sudo python SlaveMain.python` respectively.
        3. You should now see `Scan NFC Tag` on the smaller display and if you approximate your nfc tag to the reader, it should start playing music from that album / genre.
    7.  If you want to automatically run the scripts when starting your Raspberries:
        1. Open a terminal and call `cd ~/.config/lxsession/LXDE-pi/` to navigate to the LXDE config folder
        2. Open the autostart file by calling `sudo nano autostart`
        3. Now add to the end of the file:
            1. Add `@sudo /usr/bin/python2.7 /home/pi/nfcradio/projects/src/Master/MasterMain.py` (or any other version of Python 2) for the master Raspberry
            2. Add `@sudo /usr/bin/python2.7 /home/pi/nfcradio/projects/src/Slave/SlaveMain.py` (or any other version of Python 2) for the slave Raspberry
    8.  Reboot both Raspberries by unplugging / replugging them or calling `sudo reboot`
    9.  After the restart you should see `Scan NFC Tag` on the smaller display and if you approximate your nfc tag to the reader, it should start playing music from that album / genre.

# Licenses

## Music

Stance Gives You Balance by Hogan Grip is licensed under a Attribution-NonCommercial-ShareAlike 3.0 International License. [link to music](http://freemusicarchive.org/music/Hogan_Grip/Hogan_Grip_-_Stance_Gives_You_Balance/3_Stance_Gives_You_Balance).

Requiem for a Fish by The Freak Fandango Orchestra is licensed under a Attribution-NonCommercial License. [link to music](http://freemusicarchive.org/music/The_Freak_Fandango_Orchestra/Tales_Of_A_Dead_Fish/Requiem_for_a_Fish_1403).

The last ones by Jahzzar is licensed under a Attribution-ShareAlike 3.0 International License. [link to music](http://freemusicarchive.org/music/Jahzzar/Smoke_Factory/The_last_ones).

Noahs Stark by krackatoa is licensed under a Attribution-NonCommercial-ShareAlike 3.0 International License. 
Permissions beyond the scope of this license may be available at http://www.krackatoa.com or contact artist via email. [link to music](http://freemusicarchive.org/music/krackatoa/krackatoa_-_Singles_1002/Krackatoa_-_Noahs_Stark).