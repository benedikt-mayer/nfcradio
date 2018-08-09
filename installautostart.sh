run_autostart_script()
{
    ANSWER=$1
    if [ "$ANSWER" == "master" ]
        echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/projects/src/Master/MasterMain.py" >> /.config/lxsession/LXDE-pi/autostart
    elif ["$ANSWER" == "slave" ]
    then
        echo "@sudo /usr/bin/python2.7 /home/pi/nfcradio/projects/src/Slave/SlaveMain.py" >> /.config/lxsession/LXDE-pi/autostart
    else 
        echo "wrong input! please write master or slave"
        read user_input
        run_autostart_script $user_input
    fi
}

echo "setting up autostart. Are you running on the master or slave?"
read user_input
run_autostart_script $user_input