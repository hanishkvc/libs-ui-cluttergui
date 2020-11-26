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
def create_label(text, posX, posY, sizeX=-1, sizeY=-1, id="label", color=0xf0f0f0ff, backgroundColor=0x404040ff, font="Mono 32"):
    label = Clutter.Text()
    label.set_id(id)
    label.set_text(text)
    label.set_background_color(Clutter.color_from_pixel(backgroundColor))
    label.set_color(Clutter.color_from_pixel(color))
    label.set_font_name(font)
    label.set_position(posX, posY)
    if (sizeX != -1) and (sizeY != -1):
        label.set_size(sizeX, sizeY)
    return label


def create_imagebutton(imageFile, posX, posY, sizeX, sizeY, id="imagebutton"):
    btnPixbuf = GdkPixbuf.Pixbuf.new_from_file(imageFile)
    btnImage = Clutter.Image()
    pixelFormat = Cogl.PixelFormat.RGB_888
    if btnPixbuf.get_has_alpha():
        pixelFormat = Cogl.RGBA_8888
    btnImage.set_data(btnPixbuf.get_pixels(), pixelFormat, btnPixbuf.get_width(), btnPixbuf.get_height(), btnPixbuf.get_rowstride())
    imgBtn = Clutter.Actor()
    imgBtn.set_id(id)
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
        print("INFO: Button is pressed:", actor.get_id())
    return Clutter.EVENT_STOP


iCnt = 0
def handle_key_press(actor, event):
    global iCnt
    print("INFO:KeyPress:{}:{}:{}".format(actor, event.keyval, chr(event.keyval)), event.flags, event.type, event.modifier_state)
    CMDKEY_MODSTATE = (Clutter.ModifierType.SHIFT_MASK | Clutter.ModifierType.CONTROL_MASK)
    if ((event.modifier_state & CMDKEY_MODSTATE) == CMDKEY_MODSTATE):
        if (event.keyval == Clutter.KEY_A):
            lBtns[iCnt].set_scale(1, 1)
            iCnt += 1
            iCnt = iCnt % len(lBtns)
            lBtns[iCnt].set_scale(1.2, 1)
        elif (event.keyval == Clutter.KEY_Q):
            print("INFO: Bowing down gracefully")
            Clutter.main_quit()
    return Clutter.EVENT_STOP


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


# Create children and connect event handlers
label = create_label("Hello again 007", 200, 200)
stage.add_child(label)

imgBtn1 = create_imagebutton("image1.png", 100, 250, 300, 100, "ibtn1")
stage.add_child(imgBtn1)
imgBtn1.connect("button-press-event", handle_btn_press)

imgBtn2 = create_imagebutton("image1.png", 100, 50, 300, 100, "ibtn2")
stage.add_child(imgBtn2)
imgBtn2.connect("button-press-event", handle_btn_press)

lBtns = [ imgBtn1, imgBtn2 ]


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
stage.connect("button-press-event", handle_btn_press)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


