#!/usr/bin/env python3
# A simple Content Browser using Clutter
# HanishKVC, v20201205IST0922
#


import sys
import enum
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
import cluttergui as cg


if len(sys.argv) != 2:
    print("Usage: {} <path/to/ui_config_files>".format(sys.argv[0]))
    exit(1)


#### Initialise


Clutter.init()

# some required things
colorizeEffect1 = Clutter.ColorizeEffect()
colorizeEffect1.set_tint(Clutter.color_from_pixel(0xE0E0F0FF))
print(colorizeEffect1.get_tint().to_string())


#### Handle events


def handle_key_press(actor, event):
    global lPos, lYRotate
    #print("INFO:KeyPress:{}:{}:{}".format(actor, event.keyval, chr(event.keyval)), event.flags, event.type, event.modifier_state)
    #CMDKEY_MODSTATE = (Clutter.ModifierType.SHIFT_MASK | Clutter.ModifierType.CONTROL_MASK)
    CMDKEY_MODSTATE = (Clutter.ModifierType.CONTROL_MASK)
    if ((event.modifier_state & CMDKEY_MODSTATE) == CMDKEY_MODSTATE):
        if (event.keyval == Clutter.KEY_A):
            cg.listbox_select(gGUI['LBCAT'], 1, cg.SelectOffsetType.CUR)
            cg.listbox_select(gGUI['LBG1'], 1, cg.SelectOffsetType.CUR, colorizeEffect=colorizeEffect1)
        elif (event.keyval == Clutter.KEY_X):
            load_screen('audio')
        elif (event.keyval == Clutter.KEY_Q):
            print("INFO: Bowing down gracefully")
            Clutter.main_quit()
    return Clutter.EVENT_STOP


def handle_destroy(actor):
    print("INFO:destroy:WhyDear-OkOk:{}".format(actor))
    Clutter.main_quit()


def handle_target(target):
    targetType, targetLink = target.split(':')
    if targetType.upper() == "CM":
        load_contentmeta(targetLink)


def handle_lb_itemclick(actor, event):
    aID = actor.get_id()
    cg.dprint(cg.GDEBUG+1, actor, event, aID)
    lb,item = aID.split('.')
    target = gData[lb][int(item)]
    print("Handle:{}->{}:{}".format(lb, item, target))
    handle_target(target)
    return Clutter.EVENT_STOP


#### Load Things


'''
UI Template file will contain One or more of

LISTBOX_BEGIN
    T:ID gui_id
    T:PID parent_gui_id
    I:X x
    I:Y y
    I:W w
    I:H h
    I:IW w
    I:IH h
    I:PAD pad_size
    S:ORIENTATION horizontal|vertical
    S:ITEMHANDLER None|Standard
LISTBOX_END


Content metadata files will contain

CAT_BEGIN
    TAG "mytag"

    GROUP_BEGIN
        GUI "gui_id"
        ITEM "image_file" "T:dest_tag"|"CD:content_file"|"CM:metadata_file"
        ITEM "image_file" "T:dest_tag"|"CD:content_file"|"CM:metadata_file"
        ...
    GROUP_END

    GROUP_BEGIN
        GUI "gui_id"
        ITEM "image_file" "T:dest_tag"|"CD:content_file"|"CM:metadata_file"
        ITEM "image_file" "T:dest_tag"|"CD:content_file"|"CM:metadata_file"
        ...
    GROUP_END

    ...

CAT_END

NOTE: Currently the concept of TAG is not used in Content metadata files

'''


## UI


gGUI = {}
gGUIData = {}


# Create the stage
def load_background(stage, backgroundImageFile):
    stageBgndImage = cg.create_image(backgroundImageFile)
    stage.set_content(stageBgndImage)


stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Black")[1])
load_background(stage, 'Background.png')
stage.set_size(800,600)
stage.set_title("Content Browser")
gGUI['ROOT'] = stage


# setup ui
def setup_ui(sFile):
    '''
    Instantiate the specified gui elements.

    Currently it supports instantiating listboxes along with their key properties
    as well as to either add them to the main window/stage or to another listbox.

    A PID of ROOT corresponds to the main window/stage.

    One can assign from among a predefined list of itemclick handlers or ignore it.

    A line begining with # is ignored, provided it is the 1st char in the line.
    If # occurs after space char or so, then the line wont be ignored.
    '''
    f = open(sFile)
    for l in f:
        if l[0] == '#':
            continue
        l = l.strip().upper()
        print(l)
        if l == "LISTBOX_BEGIN":
            tLB = {}
        elif l.startswith("I"):
            tag = l.split(' ')[0].split(':')[1]
            val = int(l.split(' ',1)[1].strip())
            tLB[tag] = val
        elif l.startswith("T"):
            tag = l.split(' ')[0].split(':')[1]
            val = l.split(' ',1)[1].strip()
            tLB[tag] = val
        elif l.startswith("S:ORIENTATION"):
            tag = l.split(' ')[0].split(':')[1]
            val = l.split(' ',1)[1].strip()
            if val == "HORIZONTAL":
                tLB[tag] = Clutter.Orientation.HORIZONTAL
            else:
                tLB[tag] = Clutter.Orientation.VERTICAL
        elif l.startswith("S:ITEMHANDLER"):
            tag = l.split(' ')[0].split(':')[1]
            val = l.split(' ',1)[1].strip()
            if val == "NONE":
                tLB[tag] = None
            else:
                tLB[tag] = handle_lb_itemclick

        elif l == "LISTBOX_END":
            print(tLB)
            if tLB['ID'] in gGUI:
                actor = gGUI[tLB['ID']]
                actor.destroy_all_children()
                actor.destroy()
            lb = cg.create_listbox(tLB['X'],tLB['Y'], tLB['W'],tLB['H'], tLB['ORIENTATION'], iD=tLB['ID'], pad=tLB['PAD'], handle_itemclick=tLB['ITEMHANDLER'])
            if tLB['PID'] == "ROOT":
                #stage.add_child(lb)
                gGUI[tLB['PID']].add_child(lb)
            elif tLB['PID'].startswith("LB"):
                cg.listbox_append_child(gGUI[tLB['PID']], tLB['W'],tLB['H'], lb)
            gGUI[tLB['ID']] = lb
            gGUIData[tLB['ID']] = { 'IW': tLB['IW'], 'IH': tLB['IH'], 'ITEMHANDLER': tLB['ITEMHANDLER'] }
    f.close()


## Data


gData = {}


def load_contentmeta(sFile):
    '''
    Currently implemented in a simple way, such that the content metadata file requires only
    GUI and ITEM elements and nothing else like CAT_BEGIN/END or GROUND_BEGIN/END.

    GUI tells the logic to clear any existing entries/children in that GUI element.
    ANd to add any ITEM entries that follow it.

    BACKGROUND can be used to set the background image of the main screen/window/stage.

    A line begining with # is ignored, provided it is the 1st char in the line.
    If # occurs after space char or so, then the line wont be ignored.
    '''
    aID = None
    f = open(sFile)
    for l in f:
        if l[0] == '#':
            continue
        l = l.strip()
        if l.upper().startswith("GUI"):
            if aID != None:
                gData[aID] = lData
            aID = l.split(' ',1)[1].strip()
            gGUI[aID].remove_all_children()
            lData = []
        elif l.upper().startswith("ITEM"):
            la = l.split(' ')
            img = la[1]
            target = la[2]
            btn = cg.create_imagebutton(img, cg.IGNORE, cg.IGNORE, gGUIData[aID]['IW'], gGUIData[aID]['IH'], "{}.{}".format(aID, len(lData)))
            cg.listbox_append_child(gGUI[aID], gGUIData[aID]['IW'], gGUIData[aID]['IH'], btn, gGUIData[aID]['ITEMHANDLER'])
            lData.append(target)
        elif l.upper().startswith("BACKGROUND"):
            img = l.split(' ')[1]
            load_background(gGUI['ROOT'], img)
    if aID != None:
        gData[aID] = lData
    print(sFile, gData)


## Screens

def _load_screen(sUIFile, sCMFile, sTarget=None):
    '''
    Represents a Unique Screen in the App.
    sUIFile: provides the UI template for the screen
    sCMFile: provides the contents for the screen
    sTarget: If any specific Target/Content in the screen requires to be triggered, then specify.
    '''
    global gGUI
    # Clear current screen if any
    gGUI['ROOT'].remove_all_children()
    gData.clear()
    dGUI = {}
    dGUI['ROOT'] = gGUI['ROOT']
    gGUI = dGUI
    # Setup new screen
    setup_ui(sUIFile)
    cg.dprint(cg.GDEBUG, stage.get_children())
    load_contentmeta(sCMFile)
    if sTarget != None:
        target = gData[sTarget][0]
        handle_target(target)


def load_screen(screen):
    _load_screen(gScreen[screen][0], gScreen[screen][1], gScreen[screen][2])


gScreen = {}
def init_screens(dScreen, basePath):
    '''
    The specified path should contain the ui template and corresponding controls related
    contentmeta files for
        main, audio
    The main is expected to have listbox named LBCAT, whose 0th entry will be triggered,
    when the main screen is displayed.
    '''
    screens = [
        [ 'main', 'LBCAT' ],
        [ 'audio', None ] ]
    for screen in screens:
        ui = "{}/ui.{}".format(basePath, screen[0])
        cm = "{}/cm.{}".format(basePath, screen[0])
        target = screen[1]
        l = [ ui, cm, target ]
        dScreen[screen[0]] = l


# Get ready to start
init_screens(gScreen, sys.argv[1])
load_screen('main')
stage.connect("destroy", handle_destroy)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


