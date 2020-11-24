#!/usr/bin/env python3
# Test Clutter
# HanishKVC, v20201124IST1127
#
from gi.repository import Clutter


# Initialise
Clutter.init()


# Create the stage
stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Red")[1])
stage.set_size(400,400)
stage.set_title("Hello World 7")


# Handle events
def handle_btn_press(actor, event):
    print("INFO:BtnPress:{},{}".format(actor, event))
    if actor == stage:
        Clutter.main_quit()


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


# Get ready to start
stage.connect("destroy", handle_destroy)
stage.connect("button-press-event", handle_btn_press)
stage.show_all()
Clutter.main()


