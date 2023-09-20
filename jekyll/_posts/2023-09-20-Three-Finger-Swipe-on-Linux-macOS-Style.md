---
title:  "Three-Finger Swipe on Linux: macOS Style!"
date:   2023-09-20
tags: ["Bash", "Scripts", "macOS", "Touchpad", "Swipe", "Feature"]
---

# Three-Finger Swipe on Linux: macOS Style!

Man, if you're like me, you dig how macOS handles three-finger swipes to switch desktops. It's smooth, it's cool, it's where it's at. But what about us Linux folks? We want in on that action too, right?

## The Idea

The jam is simple. On macOS, a three-finger swipe on the trackpad lets you seamlessly switch between virtual desktops. It's slicker than a greased-up watermelon, let me tell you. Now, Linux ain't natively geared for that, but why should we miss out?

## The Solution

Hold tight, 'cause this is where the magic happens. We're gonna use `libinput` to catch touchpad events and `wmctrl` to switch desktops. You dig?

Before runnin' the script, make sure you've got `wmctrl` installed. If not, hit it with:

```bash
sudo apt-get install wmctrl
```
or if you're rollin' with another package manager, you know the drill.

## The Code
Here's the script in all its glory. Pay attention, 'cause this is the good stuff.

```bash
#!/bin/bash

# ----------------------------------------------------------------------------
# Script Name: three_finger_touchpad_desktop_switch.sh
# Description: Switch desktops using a 3-finger swipe gesture
# Author: github.com/pipelinedave
# Version: 1.1
# Usage: sudo sh three_finger_touchpad_desktop_switch.sh
# Note: Update the "device" variable to point to your actual input device.
# ----------------------------------------------------------------------------

# Check if wmctrl is installed
if ! command -v wmctrl &> /dev/null; then
echo "Hey, playa! wmctrl ain't installed. Get it via your package manager."
exit 1
fi

# Your touchpad device (change to your actual device)
device="/dev/input/event6"

# Start the loop and capture libinput events
echo "Looping..."

libinput debug-events --device $device | while read -r line
do
# Looking for 3-finger swipes
gesture=$(echo "$line" | grep 'GESTURE_SWIPE_UPDATE' | awk '{ print $4 }')

if [ "$gesture" = "3" ]; then
# Get the vertical direction of the swipe
direction=$(echo "$line" | grep 'GESTURE_SWIPE_UPDATE' | awk '{ print $7 }')

# If swipe is up
if [ -n "$direction" ] && (( $(echo "$direction > 0" | bc -l) )); then
echo "Direction: up"
wmctrl -s 0  # Switch to desktop 0
# If swipe is down
elif [ -n "$direction" ] && (( $(echo "$direction < 0" | bc -l) )); then
echo "Direction: down"
wmctrl -s 1  # Switch to desktop 1
fi
fi
done
```

There you have it, folks. Get this script up and running, and you'll be swiping through your Linux desktops smoother than Barry White's vocal cords. Can you dig it?
