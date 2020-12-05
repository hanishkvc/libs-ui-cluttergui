#!/usr/bin/env python3
# A simple Content Browser using Clutter
# HanishKVC, v20201205IST0922
#


import enum
# Import Clutter for use
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
import cluttergui as cg


# Initialise
Clutter.init()


# required things
colorizeEffect1 = Clutter.ColorizeEffect()
colorizeEffect1.set_tint(Clutter.color_from_pixel(0xE0E0F0FF))
print(colorizeEffect1.get_tint().to_string())


# Handle events


def handle_key_press(actor, event):
    global lPos, lYRotate
    #print("INFO:KeyPress:{}:{}:{}".format(actor, event.keyval, chr(event.keyval)), event.flags, event.type, event.modifier_state)
    #CMDKEY_MODSTATE = (Clutter.ModifierType.SHIFT_MASK | Clutter.ModifierType.CONTROL_MASK)
    CMDKEY_MODSTATE = (Clutter.ModifierType.CONTROL_MASK)
    if ((event.modifier_state & CMDKEY_MODSTATE) == CMDKEY_MODSTATE):
        if (event.keyval == Clutter.KEY_A):
            lPos, lYRotate = cg.animate_list(listBtns, lPos, lYRotate+10)
            cg.listbox_select(boxv, 1, cg.SelectOffsetType.CUR)
            cg.listbox_select(boxh, 1, cg.SelectOffsetType.CUR, colorizeEffect=colorizeEffect1)
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


# Load data

'''
LISTBOX_BEGIN
    TAG "my_tag"
    GUI "gui_id"
    X x
    Y y
    W w
    H h
    ORIENTATION horizontal|vertical

    ITEM "image_file" "T:dest_tag"|"C:content_file"
    ITEM "image_file" "T:dest_tag"|"C:content_file"

LISTBOX_END

CAT_BEGIN

CAT_END

'''

gGUI = {}

def load_lb(sFile):
    f = open(sFile)


# Create the stage
stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Black")[1])
stageBgndImage = cg.create_image("Background.png")
stage.set_content(stageBgndImage)
stage.set_size(800,600)
stage.set_title("Content Browser")


# Create children and connect event handlers

lbCat = cg.create_listbox(0,100, 128,500, Clutter.ORIENTATION.VERTICAL, id="lbCat", handle_itemclick=handle_lb_itemclick)
stage.add_child(lbCat)
gGUI['lbCat'] = lbCat

lbVert = cg.create_listbox(150,100, 600,500, Clutter.Orientation.VERTICAL, iD="lbVert", pad=20)
lbG1 = cg.create_listbox(0,0, 600,128, 128,128, Clutter.Orientation.HORIZONTAL, iD="lbG1", handle_itemclick=handle_lb_itemclick)
cg.listbox_append_child(lbVert, 600,128, lbG1)
gGUI['lbG1'] = lbG1
lbG2 = cg.create_listbox(0,0, 600,128, 128,128, Clutter.Orientation.HORIZONTAL, iD="lbG2", handle_itemclick=handle_lb_itemclick)
cg.listbox_append_child(lbVert, 600,128, lbG2)
gGUI['lbG2'] = lbG2
stage.add_child(lbVert)


# Get ready to start
stage.connect("destroy", handle_destroy)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


