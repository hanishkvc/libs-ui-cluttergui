#!/usr/bin/env python3
# ClutterMedia - A simple media player for clutter

from gi.repository import Gst
from gi.repository import ClutterGst


def init():
    #Gst.init()
    ClutterGst.init()


gPlayer = None
gPlayType = '?'
gVideoContentUI = None
def play_audio(sFile):
    global gPlayer, gPlayType
    stop()
    print("INFO:CM:PlayA", sFile)
    gPlayer = ClutterGst.Playback()
    gPlayer.set_filename(sFile)
    gPlayer.set_audio_volume(0.6)
    gPlayer.set_playing(True)
    gPlayType = 'A'


def pause():
    if (gPlayer != None) and (gPlayType != '?'):
        gPlayer.set_playing(False)


def unpause():
    if (gPlayer != None) and (gPlayType != '?'):
        gPlayer.set_playing(True)


def stop(cleanup=False):
    global gPlayType
    if gPlayer != None:
        print("INFO:CM:Stop in case")
        gPlayer.set_playing(False)
        gPlayType = '?'
        if cleanup:
            pass


def play_video(sFile, ui):
    global gPlayer, gPlayType
    stop()
    print("INFO:CM:PlayV", sFile)
    gPlayer = ClutterGst.Playback()
    gPlayer.set_filename(sFile)
    gPlayer.set_audio_volume(0.6)
    cgstContent = ClutterGst.Aspectratio()
    cgstContent.set_player(gPlayer)
    ui.set_content(cgstContent)
    gVideoContentUI = cgstContent
    #ui.show()
    # default content gravity is resize fill, so things should be fine.
    # need to check, if I require to set the scaling filters explicitly or default is good enough.
    gPlayer.set_playing(True)
    gPlayType = 'V'

