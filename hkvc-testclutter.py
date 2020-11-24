#!/usr/bin/env python3
# Test Clutter
# HanishKVC, v20201124IST1127
#


# Import Clutter for use
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf
from gi.repository import Cogl

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
label.set_background_color(Clutter.Color.new(0x80, 0x80, 0x80, 0xff))
label.set_color(Clutter.color_from_string("#0000ff80")[1])
label.set_color(Clutter.color_from_pixel(0x00ff0080))
label.set_font_name("Mono 32")
label.set_position(200, 200)
stage.add_child(label)

btnPixbuf = GdkPixbuf.Pixbuf.new_from_file("image1.png")
btnImage = Clutter.Image()
btnImage.set_data(btnPixbuf.get_pixels(), Cogl.PixelFormat.RGB_888, btnPixbuf.get_width(), btnPixbuf.get_height(), btnPixbuf.get_rowstride())
imgBtn = Clutter.Actor()
imgBtn.set_content(btnImage)
imgBtn.set_content_scaling_filters(Clutter.ScalingFilter.LINEAR, Clutter.ScalingFilter.LINEAR)
imgBtn.set_content_gravity(Clutter.Gravity.CENTER)
imgBtn.set_position(100, 300)
stage.add_child(imgBtn)


# Handle events
def handle_btn_press(actor, event):
    print("INFO:BtnPress:{},{}".format(actor, event))
    if actor == stage:
        Clutter.main_quit()


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
stage.connect("button-press-event", handle_btn_press)
stage.show()
Clutter.main()


