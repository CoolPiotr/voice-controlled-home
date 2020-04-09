#!/usr/bin/python3

# Developed on Python 3.8.2


"""
# use VLC for playback

import vlc
import time

talk = vlc.MediaPlayer("/home/pi/Bronski Beat - Smalltown Boy.mp3")

talk.play()

time.sleep(10)
"""


# use mpg123 for playback
# Note: without adding .wait() to the proc, this script will terminate but sound will keep playing.

import subprocess
import time

def play_mp3(path):
	return subprocess.Popen(['mpg123', '-q', path])

import pulsectl

with pulsectl.Pulse("test-rig") as pulse:
	print( pulse.sink_list() )
	print( pulse.source_list() )
print()

proc1 = play_mp3("/home/pi/Bronski Beat - Smalltown Boy.mp3")
time.sleep(4)
print( proc1.poll() )
proc2 = play_mp3("/home/pi/CoolPiotr/voice-controlled-home/experiment/output.mp3")
with pulsectl.Pulse("test-rig") as pulse:
	print( pulse.sink_list() )
	print( pulse.source_list() )
print()

time.sleep(4)
print( proc2.poll() )
proc2.kill()
time.sleep(4)
proc1.kill()



