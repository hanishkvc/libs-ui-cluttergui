#!/usr/bin/env python3
# Test Clutter
# HanishKVC, v20201124IST1127
#


import enum
# Import Clutter for use
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
from gi.repository import Cogl
import cluttergui as cg


# Initialise
Clutter.init()


# Handle events
def handle_btn_press(actor, event):
    print("INFO:BtnPress:{},{}".format(actor, event))
    print("\t x,y [{},{}], btn [{}]".format(event.x, event.y, event.button))
    if actor == stage:
        print("INFO: Bowing down gracefully")
        Clutter.main_quit()
    elif actor in (imgBtn1, imgBtn2):
        print("INFO: Button is pressed:", actor.get_id())
    return Clutter.EVENT_STOP


def handle_key_press(actor, event):
    global lPos, lYRotate
    print("INFO:KeyPress:{}:{}:{}".format(actor, event.keyval, chr(event.keyval)), event.flags, event.type, event.modifier_state)
    CMDKEY_MODSTATE = (Clutter.ModifierType.SHIFT_MASK | Clutter.ModifierType.CONTROL_MASK)
    if ((event.modifier_state & CMDKEY_MODSTATE) == CMDKEY_MODSTATE):
        if (event.keyval == Clutter.KEY_A):
            lPos, lYRotate = animate_list(listBtns, lPos, lYRotate+10)
            listbox_select(boxv, 1, SelectOffsetType.CUR)
            listbox_select(boxh, 1, SelectOffsetType.CUR, colorizeEffect=colorizeEffect1)
        elif (event.keyval == Clutter.KEY_Q):
            print("INFO: Bowing down gracefully")
            Clutter.main_quit()
    return Clutter.EVENT_STOP


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


def handle_lb_itemclick(actor, event):
    aID = actor.get_id()
    print(actor, event, aID)
    return Clutter.EVENT_STOP


# Create the stage
stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Black")[1])
stageBgndImage = create_image("Background.png")
stage.set_content(stageBgndImage)
stage.set_size(800,600)
stage.set_title("Hello World 7")


# Create children and connect event handlers
label = create_label("Hello again 007", 400, 20)
stage.add_child(label)

imgBtn1 = create_imagebutton("image1.png", 100, 450, 300, 100, "ibtn1")
stage.add_child(imgBtn1)
imgBtn1.connect("button-press-event", handle_btn_press)
imgBtn2 = create_imagebutton("image1.png", 400, 450, 300, 100, "ibtn2")
stage.add_child(imgBtn2)
imgBtn2.connect("button-press-event", handle_btn_press)
lPos = 0
lYRotate = 0
listBtns = [ imgBtn1, imgBtn2 ]

images = [ "Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png" ]
boxv = create_listbox_imagebuttons(images, 2,2, 128,128*4, 128,128, Clutter.Orientation.VERTICAL, id="cat", handle_itemclick=handle_lb_itemclick)
boxv.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, 40)
stage.add_child(boxv)
# Overwriting/Reusing the boxh below, so only the last listbox will be animated
images = [ "Item1.png", "Item2.png", "Item3.png", "Item4.png", "Item5.png", "Item6.png", "Item7.png" ]
boxh = create_listbox_imagebuttons(images, 132,100, 128*6,128, 128,128, Clutter.Orientation.HORIZONTAL, id="il1", handle_itemclick=handle_lb_itemclick)
stage.add_child(boxh)
boxh = create_listbox_imagebuttons(images, 132,240, 128*6,32, 128,128, Clutter.Orientation.HORIZONTAL, id="il2", handle_itemclick=handle_lb_itemclick)
stage.add_child(boxh)
images = [ "Item11.png", "Item12.png", "Item13.png", "Item14.png", "Item15.png", "Item16.png", "Item17.png" ]
boxh = create_listbox_imagebuttons(images, 132,284, 128*6,128, 128,128, Clutter.Orientation.HORIZONTAL)
stage.add_child(boxh)


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
#stage.connect("button-press-event", handle_btn_press)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


