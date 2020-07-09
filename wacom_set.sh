#!/bin/rc
{
    sleep 2

    if (~ $DISPLAY ()) {
        DISPLAY=:0
        XAUTHORITY=/home/lcp/.Xauthority
    }

    #xsetwacom set 'Wacom Intuos PT S Pad pad' button 9 'button +3 -3'
    #xsetwacom set 'Wacom Intuos PT S Pad pad' button 8 'button +4 -4'
    #xsetwacom set 'Wacom Intuos PT S Pad pad' button 3 'button +1 -1'
    #xsetwacom set 'Wacom Intuos PT S Pad pad' button 1 'button +2 -2'
    /bin/xsetwacom --set 'Wacom Intuos Pro M Finger touch' touch off
    /bin/xsetwacom --set 'Wacom Intuos Pro M (WL) Finger touch' touch off

} &
