# NFC Timeline Radio
This is the software written for the NFC Timeline Radio featured on [instructables.com](https://www.instructables.com/id/NFC-Timeline-Radio/).

# Software Installation Instructions
1. Arduino software
    1. Create an account on [Arduino Create](https://create.arduino.cc/).
    2. Install the Arduino Create plugin from [here](https://create.arduino.cc/getting-started/plugin).
    3. Retrieve your nfc tag UID
        1. Now load the sketch [`read_nfc_tag`](https://create.arduino.cc/editor/banjo8/8b9f83ed-a522-4f10-be2b-dee91c7dc1d6/preview) to the arduino while connected to your computer.
        2. Approximate your nfc tag / card to the nfc reader.
        3. Look at the Monitor on the left of the editor for a UID: it looks like this `CE 2F F1 D9`, but can be shorter or longer
    4. Now that you have your UID, modify the sketch [`read_rfid_potentiometer`](https://create.arduino.cc/editor/banjo8/8237c80f-99fb-4187-8e98-c224d42e4b03/preview)
        1. Replace the UIDs in line 115 and 122 with your UIDs. One is enough, two are better so that you can change albums / genres.
        2. Save and upload the script to the Arduino.
        3. Now connect the Arduino to your Master Raspberry Pi and reboot the Pi.
2. Raspberry software
    1. Get "Raspbian Stretch with Desktop" from and follow instructions on https://www.raspberrypi.org/downloads/raspbian/.
    2. To set up some options, open a terminal and run `sudo raspi-config`:
        1. In the settings, select **Interfacing Options** -> **I2C** -> **Yes**, to start up the I2C core driver.
        2. Now select **Interfacing Options** -> **SPI** -> **Yes** to enable SPI.
        3. Go to **Network Options** -> **Wi-fi**, now enter the **SSID** and **password** of your access point / router. Now you have a internet connection to install software!
        4. The serial port of RPi is set to serial terminal debugging function mode by default. If you want the serial port services as a common IO, you should modify the settings on the RPi.  
        Go to **Interfacing Options** -> **Serial** and select **No** in the first and **Yes** in the second dialog.
        1. Press `Finish` to save the settings. This will prompt you to reboot.
    3. When logged into the Raspberries, open a terminal and from the home repository of your raspberry (`~`, default is `/home/pi`), pull the source code from [Github](https://github.com/benedikt-mayer/nfcradio) by e.g. calling `git clone https://github.com/benedikt-mayer/nfcradio.git`.
    4. Run the shell script in the root repository of the git folder by opening a terminal and running `sudo sh install.sh` to install all necessary python libraries, setting config files etc.  
       This will reboot the device at the end. Don't interrupt the script unless you are prompted (which you will be).
    5. After the restart you should see `Scan NFC Tag` on the smaller display: If you now approximate your nfc tag to the reader, it should start playing music from that album / genre.

# Licenses

## Music

Stance Gives You Balance by Hogan Grip is licensed under a Attribution-NonCommercial-ShareAlike 3.0 International License. [link to music](http://freemusicarchive.org/music/Hogan_Grip/Hogan_Grip_-_Stance_Gives_You_Balance/3_Stance_Gives_You_Balance).

Requiem for a Fish by The Freak Fandango Orchestra is licensed under a Attribution-NonCommercial License. [link to music](http://freemusicarchive.org/music/The_Freak_Fandango_Orchestra/Tales_Of_A_Dead_Fish/Requiem_for_a_Fish_1403).

The last ones by Jahzzar is licensed under a Attribution-ShareAlike 3.0 International License. [link to music](http://freemusicarchive.org/music/Jahzzar/Smoke_Factory/The_last_ones).

Noahs Stark by krackatoa is licensed under a Attribution-NonCommercial-ShareAlike 3.0 International License. 
Permissions beyond the scope of this license may be available at http://www.krackatoa.com or contact artist via email. [link to music](http://freemusicarchive.org/music/krackatoa/krackatoa_-_Singles_1002/Krackatoa_-_Noahs_Stark).


The Boss by Dee Yan-Key is licensed under a Attribution-NonCommercial-ShareAlike License. [link to music](http://freemusicarchive.org/music/Dee_Yan-Key/Fast_Swing_reloaded/07--Dee_Yan-Key-The_Boss).

The Pianist by Dee Yan-Key is licensed under a Attribution-NonCommercial-ShareAlike License. [link to music](http://freemusicarchive.org/music/Dee_Yan-Key/Summer_Nights/11--Dee_Yan-Key-The_Pianist).

Hungaria by Latché Swing is licensed under a Attribution-Noncommercial-Share Alike 2.0 France License. [link to music](http://freemusicarchive.org/music/Latch_Swing/demo_2008/Hungaria).

Little Lily Swing by Tri-Tachyon is licensed under a Attribution License. [link to music](http://freemusicarchive.org/music/Tri-Tachyon/Little_Lily_Swing/Tri-Tachyon_-_01_-_Little_Lily_Swing).

Kelli's Number by U.S. Army Blues is licensed under a Public Domain Mark 1.0 License. [link to music](http://freemusicarchive.org/music/US_Army_Blues/Live_At_Blues_Alley/0_-_08_-_The_US_Army_Blues_-_Kellis_Number).
