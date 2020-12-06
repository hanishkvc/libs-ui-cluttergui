#!/usr/bin/env python3
# ClutterMedia - A simple media player for clutter

from gi.repository import Gst
from gi.repository import ClutterGst


def init():
    #Gst.init()
    ClutterGst.init()


gPlayer = None
def play_audio(sFile):
    global gPlayer
    stop()
    print("INFO:CM:Play", sFile)
    gPlayer = ClutterGst.Playback()
    gPlayer.set_filename(sFile)
    gPlayer.set_audio_volume(0.6)
    gPlayer.set_playing(True)


def stop():
    if gPlayer != None:
        print("INFO:CM:Stop in case")
        gPlayer.set_playing(False)


