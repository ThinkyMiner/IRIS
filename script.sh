#!/bin/bash

# Define the song name to search
song_name="Aasa Kooda"

# Open Music app, search for the song, and play it
osascript <<EOF
tell application "Music"
    activate
    delay 1
    set search_string to "$song_name"
    tell application "System Events"
        keystroke "f" using {command down}
        delay 1
        keystroke search_string
        delay 2
        key code 125 -- Arrow down to select the first song in the results
        delay 1
        key code 125 -- Arrow down to select the first song in the results
        delay 1
        key code 36 -- Presses Enter to play the selected song
    end tell
end tell
EOF
