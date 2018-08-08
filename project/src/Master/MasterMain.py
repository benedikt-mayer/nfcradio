import serial
import pygame
import time
import re  # regular expressions
import RPi.GPIO as gpio
import epd1in54
import Image
import ImageDraw
import ImageFont
import threading

from pygame.locals import *

pygame.init()
pygame.display.set_mode((400, 300))
pygame.mixer.init(44100, -16, 2, 2048)

# setup for play/pause button
gpio.setmode(gpio.BCM)
gpio.setup(13, gpio.IN, pull_up_down=gpio.PUD_UP)

MUSICPATH = "/home/pi/PEM2/project/resources/music/"

songs = {
    "1": [
        {
            "name": "Rock/Stance_Gives_You_Balance.mp3",
            "year": "2010"
        },
        {
            "name": "Rock/Requiem_for_a_Fish.mp3",
            "year": "2011"
        },
        {
            "name": "Rock/The_last_ones.mp3",
            "year": "2012"
        },
        {
            "name": "Rock/Noahs_Stark.mp3",
            "year": "2013"
        }
    ],
    "2": [
        {
            "name": "Jazz/Hungaria.mp3",
            "year": "2009"
        },
        {
            "name": "Jazz/Kellis_Number.mp3",
            "year": "2013"
        },
        {
            "name": "Jazz/Little_Lily_Swing.mp3",
            "year": "2015"
        },
        {
            "name": "Jazz/The_Boss.mp3",
            "year": "2017"
        },
        {
            "name": "Jazz/The_Pianist.mp3",
            "year": "2018"
        }
    ]
}

album = ""
MAXSONGVALUE = 100
lastSongName = ""
lastAlbum = ""
playing = True
songIncrements = 0.0
BEGINMESSAGE = "Scan NFC Tag"

# Inner Subclass of threading module to put display updating off the main thread
# Start Thread by calling mythread.start() which in turn invokes run()

class DisplayThread (threading.Thread):

    def __init__(self, threadID, name, songName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.songName = songName

    def displaySong(self, threadName, songName):
        # initialise the display
        epd = epd1in54.EPD()
        epd.init(epd.lut_full_update)
        # For simplicity, the arguments are explicit numerical coordinates
        # 255: clear the frame
        image = Image.new(
            '1', (epd1in54.EPD_HEIGHT, epd1in54.EPD_WIDTH), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)

        # get the display name of the song, which has just the name without underscores or file type
        if songName != BEGINMESSAGE:
            slashIndex = songName.index("/") + 1
            dotIndex = songName.index(".mp3")
            songDisplayName = songName[slashIndex:dotIndex].replace(
                "_", " ").replace("1-", "")
        else:
            songDisplayName = songName

        # get the textSize as a (widht, height) tuple
        textSize = draw.textsize(songDisplayName, font=font)

        # calculate the x and y position based on the display and text dimensions
        xPosition = (epd1in54.EPD_HEIGHT - textSize[0]) / 2
        yPosition = (epd1in54.EPD_WIDTH - textSize[1]) / 2

        # draw the song name at the appropriate spot, which is in the middle
        draw.text((xPosition, yPosition), songDisplayName, font=font, fill=0)

        # rotate the current image
        rotatedImage = image.rotate(90, expand=1)

        # send the image to the display
        epd.clear_frame_memory(0xFF)
        epd.set_frame_memory(rotatedImage, 0, 0)
        epd.display_frame()

    def run(self):
        print "Starting " + self.name
        self.displaySong(self.name, self.songName)
        print "Exiting " + self.name


def playSong(songName):
    pygame.mixer.music.load(MUSICPATH + songName)
    pygame.mixer.music.set_volume(0.0)
    pygame.mixer.music.play()

# display a message at the beginning, when the device is turned on.
thread = DisplayThread(1, "Thread-Display", BEGINMESSAGE)
thread.start()

while True:

    try:
        # connection to arduino
        arduino = serial.Serial("/dev/ttyACM0", 9600)
        arduinoData = arduino.readline()
        # connection to second raspberry
        raspberrySlave = serial.Serial("/dev/ttyS0", 115200)
    except:
        print("oh no. raspberry or arduino not found.")
        continue

    # button press for play / pause
    buttonPressed = gpio.input(13)
    if buttonPressed == 0:
        if playing:
            # check if the song is still going, if yes pause it otherwise play again
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.pause()
                playing = False
        else:
            pygame.mixer.music.unpause()
            playing = True
        # this is so that we don't keep toggeling.
        time.sleep(1)

    # now check what arduino has sent. if it's a uid, set the album accordingly
    if "uid" in arduinoData:
        if "1" in arduinoData:
            album = "1"
        elif "2" in arduinoData:
            album = "2"
        # needs to be a float
        songIncrements = float(MAXSONGVALUE) / float(len(songs.get(album)))

    # check if the album has changed since the last time.
    if (lastAlbum != album) and (album != ""):
        # display songs of select album on large screen
        raspberrySlave.write("displaysongs album: " + album + "\n")
        lastAlbum = album

    # see if there is any information about potentiometers, e.g. volume or song changes
    if ("potentiometer" in arduinoData) and (album != ""):
        # deduct one so that we have 0-99 and rounding works properly. if this leads to negative values, just take 0.
        potentiometerValue = int(re.findall(r'\d+', arduinoData)[0])-1
        number = potentiometerValue if (potentiometerValue >= 0) else 0

        # if arduino has sent volume information, change it accordingly
        if "volume" in arduinoData:
            # print("volume is set to " + str(number))
            pygame.mixer.music.set_volume(float(number) / 100)
        # otherwise if the arduino has sent song information, check if we need to change song
        elif "song" in arduinoData:
            # retrieve the name of the current song, for which we need the index of the song
            songIndex = int(number / songIncrements)
            songName = songs[album][songIndex]["name"]
            # check if the song has changed
            if lastSongName != songName:
                # Asynchroniously display the song name on the small display so playing of songs is not blocked
                thread = DisplayThread(1, "Thread-Display", songName)
                thread.start()
                # play the song
                playSong(songName)
                # set the lastSongName, so that we know which song is playing
                lastSongName = songName