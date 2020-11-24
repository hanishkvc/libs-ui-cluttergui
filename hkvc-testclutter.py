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
stage.set_size(600,400)
stage.set_title("Hello World 7")


# Create children
label = Clutter.Text()
label.set_text("Hello again 007")
label.set_color(Clutter.Color.new(0x00, 0x00, 0xff, 0xff))
label.set_color(Clutter.color_from_string("#0000ff80")[1])
label.set_color(Clutter.color_from_pixel(0x00ff0080))
label.set_font_name("Mono 32")
label.set_position(200, 200)
stage.add_child(label)


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


