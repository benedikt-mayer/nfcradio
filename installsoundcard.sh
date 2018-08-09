sudo touch /etc/asound.conf
sudo echo "pcm.!default { \n    type hw \n    card 1 \n} \n \nctl.!default { \n    type hw \n    card 1 \n} \n" >> /etc/asound.conf