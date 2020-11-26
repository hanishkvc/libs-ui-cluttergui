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


# Widget helpers
def create_label(text, posX, posY, color=0xf0f0f0ff, backgroundColor=0x404040ff, font="Mono 32"):
    label = Clutter.Text()
    label.set_text(text)
    label.set_background_color(Clutter.color_from_pixel(backgroundColor))
    label.set_color(Clutter.color_from_pixel(color))
    label.set_font_name(font)
    label.set_position(posX, posY)
    return label


def create_imagebutton(imageFile, posX, posY, sizeX, sizeY):
    btnPixbuf = GdkPixbuf.Pixbuf.new_from_file(imageFile)
    btnImage = Clutter.Image()
    pixelFormat = Cogl.PixelFormat.RGB_888
    if btnPixbuf.get_has_alpha():
        pixelFormat = Cogl.RGBA_8888
    btnImage.set_data(btnPixbuf.get_pixels(), pixelFormat, btnPixbuf.get_width(), btnPixbuf.get_height(), btnPixbuf.get_rowstride())
    imgBtn = Clutter.Actor()
    imgBtn.set_content(btnImage)
    imgBtn.set_content_scaling_filters(Clutter.ScalingFilter.LINEAR, Clutter.ScalingFilter.LINEAR)
    imgBtn.set_content_gravity(Clutter.Gravity.CENTER)
    imgBtn.set_position(posX, posY)
    imgBtn.set_size(sizeX, sizeY)
    imgBtn.set_reactive(True)
    return imgBtn


# Handle events
def handle_btn_press(actor, event):
    print("INFO:BtnPress:{},{}".format(actor, event))
    if actor == stage:
        print("INFO: Bowing down gracefully")
        Clutter.main_quit()
    elif actor in (imgBtn1, imgBtn2):
        print("INFO: Button is pressed")
    return Clutter.EVENT_STOP


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


# Create children and connect event handlers
label = create_label("Hello again 007", 200, 200)
stage.add_child(label)

imgBtn1 = create_imagebutton("image1.png", 100, 250, 300, 100)
stage.add_child(imgBtn1)
imgBtn1.connect("button-press-event", handle_btn_press)

imgBtn2 = create_imagebutton("image1.png", 100, 50, 300, 100)
stage.add_child(imgBtn2)
imgBtn2.connect("button-press-event", handle_btn_press)


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
stage.connect("button-press-event", handle_btn_press)
stage.show()
Clutter.main()


