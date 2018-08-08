import RPi.GPIO as GPIO
import serial
import time
import epd7in5b
import Image
import ImageDraw
import ImageFont

connected = False

# only run the rest of the code once the master raspberry has been connected
while not connected:
    try:
        # connection to second raspberry
        raspberryMaster = serial.Serial("/dev/ttyS0", 115200)
        connected = True
    except: 
        print("oh no. raspberry master not found.")


EPD_WIDTH = 640
EPD_HEIGHT = 384

BEGIN_LEFT = 80
END_RIGHT = 560
AVAILABLE_WIDTH = END_RIGHT - BEGIN_LEFT
widthPerSong = 0

BEGIN_TOP = 42
END_BOTTOM = 300
AVAILABLE_HEIGHT = END_BOTTOM - BEGIN_TOP
heightPerSong = 0

RECTANGLE_HEIGHT = 15
RECTANGLE_Y_OFFSET = 5

TIMELINE_HEIGHT = 5
TIMELINE_Y_OFFSET = 20

TICK_WIDTH = 4
TICK_HEIGHT = 20

YEAR_Y_OFFSET = 4

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

def displaySongs(command):
    epd = epd7in5b.EPD()
    epd.init()

    album = command.replace("displaysongs album: ", "").replace("\n", "")

    songlist = songs[album]

    image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT),
                      255)    # 255: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)

    widthPerSong = AVAILABLE_WIDTH / len(songlist)
    heightPerSong = AVAILABLE_HEIGHT / len(songlist)

    for song in songlist:
        index = songlist.index(song)
        songName = song["name"]
        songYear = song["year"]

        slashIndex = songName.index("/") + 1
        dotIndex = songName.index(".mp3")
        
        songDisplayName = songName[slashIndex:dotIndex].replace(
            "_", " ").replace("1-", "")

        positionLeft = BEGIN_LEFT + index * widthPerSong
        positionRight = BEGIN_LEFT + (index+1) * widthPerSong
        positionTop = BEGIN_TOP + RECTANGLE_Y_OFFSET + index * heightPerSong
        positionBottom = BEGIN_TOP + RECTANGLE_Y_OFFSET + \
            RECTANGLE_HEIGHT + index * heightPerSong

        xPositionCentered = positionLeft + (widthPerSong / 2)

        songTextSize = draw.textsize(songDisplayName, font=font)
        yearTextSize = draw.textsize(songYear, font=font)

        textXPosition = xPositionCentered - (songTextSize[0] / 2)
        textYPosition = positionTop - RECTANGLE_Y_OFFSET - RECTANGLE_HEIGHT

        tickXPosition = xPositionCentered - (TICK_WIDTH / 2)
        tickYPosition = END_BOTTOM + TIMELINE_Y_OFFSET - (TICK_HEIGHT / 2)

        yearXPosition = xPositionCentered - (yearTextSize[0] / 2)
        yearYPosition = tickYPosition + TICK_HEIGHT + YEAR_Y_OFFSET

        # large rectangle
        draw.rectangle((positionLeft, positionTop,
                        positionRight, positionBottom), fill=0)
        # timeline rectangle
        draw.rectangle((tickXPosition, tickYPosition, tickXPosition +
                        TICK_WIDTH, tickYPosition + TICK_HEIGHT), fill=0)
        # song name
        draw.text((textXPosition, textYPosition),
                  songDisplayName, font=font, fill=0)
        # year name
        draw.text((yearXPosition, yearYPosition), songYear, font=font, fill=0)

    timelineYPosition = END_BOTTOM + TIMELINE_Y_OFFSET - (TIMELINE_HEIGHT / 2)

    draw.rectangle((BEGIN_LEFT, timelineYPosition, END_RIGHT,
                    timelineYPosition + TIMELINE_HEIGHT), fill=0)

    # For simplicity, the arguments are explicit numerical coordinates
    epd.display_frame(epd.get_frame_buffer(image))

while True:
    command = raspberryMaster.readline()

    print(command)

    if "displaysongs" in command:
        displaySongs(command)