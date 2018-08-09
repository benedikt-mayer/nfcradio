if ! grep -Pq "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" /etc/asound.conf
then
    touch /etc/asound.conf
    echo "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" >> /etc/asound.conf
    amixer set PCM 80%
else 
    echo "soundcard configuration data already added"
fi