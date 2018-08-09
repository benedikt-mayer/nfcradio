run_autostart_script()
{
    ANSWER=$1
    if [ "$ANSWER" = "master" ]
    then
        echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Master/MasterMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
    elif [ "$ANSWER" = "slave" ]
    then
        echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/project/src/Slave/SlaveMain.py" >> /home/pi/.config/lxsession/LXDE-pi/autostart
    else 
        echo "wrong input! please write master or slave"
        read user_input
        run_autostart_script $user_input
    fi
}

echo "setting up autostart. Are you running on the master or slave?"
read user_input
run_autostart_script $user_input