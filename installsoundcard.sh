sudo touch /etc/asound.conf
echo "pcm.!default { \n    type hw \n    card 1 \n} \n \n ctl.!default { \n    type hw \n    card 1 \n } \n" >> /etc/asound.conf