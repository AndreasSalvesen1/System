#!/bin/bash

# Start Visual Studio Code with in-process GPU
code --in-process-gpu &&
sleep 1
wmctrl -r "code" -b add,maximized_vert,maximized_horz

# Start Firefox in full screen mode
firefox &

# Start Steam in big picture mode (which is fullscreen)
steam &

#Starter Spotifyx
spotify &
sleep 1
wmctrl -r "Spotify" -b add,maximized_vert,maximized_horz

#Starter discord
sleep 5
discord