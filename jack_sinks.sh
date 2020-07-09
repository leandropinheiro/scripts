#/bin/bash

pactl load-module module-jack-sink client_name=Jack_Discord connect=yes
pactl load-module module-jack-sink client_name=Jack_Monitor connect=yes
pactl load-module module-jack-source client_name=Jack_IN1 connect=no
pactl load-module module-jack-source client_name=Jack_IN2 connect=no
pactl load-module module-jack-source client_name=Jack_IN3 connect=no
