#!/usr/bin/env python3
# Clutter based SIMPLE GUI Library
# HanishKVC, v20201124IST1127
#


import enum
## Import Clutter for use
import gi
from gi.repository import GLib
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf
from gi.repository import Pango, Cogl
import time


## Initialise

pathData = "data/"
Clutter.init()


## data loading helpers

def load_pixbuf(imageFile):
    '''
    create a pixbuf from specified image in the data directory
    '''
    imageFile = "{}/{}".format(pathData, imageFile)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(imageFile)
    return pixbuf


## Widget helpers

gActors = {}
blurEffect = Clutter.BlurEffect()
IGNORE=-99

# Labels

def create_label(text, posX, posY, sizeX=IGNORE, sizeY=IGNORE, iD="label", color=0xf0f0f0ff, backgroundColor=0x404040ff, font="Mono 32"):
    label = Clutter.Text()
    label.set_id(iD)
    label.set_text(text)
    label.set_background_color(Clutter.color_from_pixel(backgroundColor))
    label.set_color(Clutter.color_from_pixel(color))
    label.set_font_name(font)
    '''
    x = label.get_layout()
    x.set_alignment(Pango.Alignment.CENTER)
    print(x.get_alignment(), x.get_text())
    x.set_spacing(50)
    x.set_justify(True)
    label.set_content_gravity(Clutter.Gravity.CENTER)
    label.set_line_alignment(Pango.Alignment.CENTER)
    label.set_justify(True)
    label.set_anchor_point(20,20)
    '''
    if (posX != IGNORE) and (posY != IGNORE):
        label.set_position(posX, posY)
    if (sizeX != IGNORE) and (sizeY != IGNORE):
        label.set_size(sizeX, sizeY)
    return label


# Images

def create_image(imageFile):
    pixbuf = load_pixbuf(imageFile)
    image = Clutter.Image()
    pixelFormat = Cogl.PixelFormat.RGB_888
    if pixbuf.get_has_alpha():
        pixelFormat = Cogl.PixelFormat.RGBA_8888
    image.set_data(pixbuf.get_pixels(), pixelFormat, pixbuf.get_width(), pixbuf.get_height(), pixbuf.get_rowstride())
    return image


# Buttons

def create_imagebutton(imageFile, posX, posY, sizeX, sizeY, iD="imagebutton"):
    btnImage = create_image(imageFile)
    imgBtn = Clutter.Actor()
    imgBtn.set_id(iD)
    imgBtn.set_content(btnImage)
    imgBtn.set_content_scaling_filters(Clutter.ScalingFilter.LINEAR, Clutter.ScalingFilter.LINEAR)
    imgBtn.set_content_gravity(Clutter.Gravity.CENTER)
    if (posX != IGNORE) and (posY != IGNORE):
        imgBtn.set_position(posX, posY)
    if (sizeX != IGNORE) and (sizeY != IGNORE):
        imgBtn.set_size(sizeX, sizeY)
    imgBtn.set_reactive(True)
    return imgBtn


def create_button(posX, posY, sizeX, sizeY, imageFile=None, text=None, iD="button",
                    textColor=0xf0f0f0ff, textBackgroundColor=0x404040ff, textFont="Mono 28"):
    if imageFile != None:
        btn = create_imagebutton(imageFile, posX, posY, sizeX, sizeY, iD)
    elif text != None:
        btn = create_label(text, posX, posY, sizeX, sizeY, iD, textColor, textBackgroundColor, textFont)
    btn.set_content_gravity(Clutter.Gravity.CENTER)
    btn.set_reactive(True)
    return btn


# ListBoxs

LB_CLEANUP_TIMEOUT = 700
def _lb_scroll_cleanup(actor):
    #print("lbScrollCleanup:", actor)
    aID = actor.get_id()
    if gActors[aID]['blur']:
        actor.remove_effect(blurEffect)
        gActors[aID]['blur'] = False
    return False


LB_GESTURE_DELTATIME_MS = 0.500
gLBMMCnt = 0
def _handle_lb_mouse(actor, event):
    global gLBMMCnt
    #print("INFO:LbMouse:{}:{}:{},{}:{}".format(event.time, actor, event.x, event.y, event.type))
    aID = actor.get_id()
    orientation = actor.get_layout_manager().get_orientation()
    if event.type == Clutter.EventType.BUTTON_PRESS:
        print("DBUG:LBMouse:BtnPress", aID, gLBMMCnt)
        gActors[aID]['prevPos'] = (event.x, event.y)
        gActors[aID]['prevTime'] = time.time()
        return Clutter.EVENT_PROPAGATE
    elif event.type == Clutter.EventType.MOTION:
        gLBMMCnt += 1
        prevPos = gActors[aID]['prevPos']
        prevTime = gActors[aID]['prevTime']
        x = gActors[aID]['posX']
        y = gActors[aID]['posY']
        if prevTime != None:
            timeDelta = time.time() - prevTime
        else:
            timeDelta = 54321
        if (timeDelta < LB_GESTURE_DELTATIME_MS):
            xD = event.x - prevPos[0]
            yD = event.y - prevPos[1]
            if abs(xD) > abs(yD):
                x -= xD
            else:
                y -= yD
            if (x >= 0) and (y >= 0):
                if ((orientation == Clutter.Orientation.HORIZONTAL) and (x > 0)) or ((orientation == Clutter.Orientation.VERTICAL) and (y > 0)):
                    actor.save_easing_state()
                    point = Clutter.Point()
                    point.x = x
                    point.y = y
                    actor.scroll_to_point(point)
                    gActors[aID]['posX'] = x
                    gActors[aID]['posY'] = y
                    actor.restore_easing_state()
                else:
                    print("DBUG:LBMouse:Motion: Not my scroll", aID, gLBMMCnt)
                    return False
            else:
                if ((orientation == Clutter.Orientation.HORIZONTAL) and (x < 0)) or ((orientation == Clutter.Orientation.VERTICAL) and (y < 0)):
                    print("DBUG:LBMouse:Motion: Scroll already at boundry", aID, gLBMMCnt, x, y)
                    if gActors[aID]['blur'] == False:
                        actor.add_effect(blurEffect)
                        gActors[aID]['blur'] = True
                        Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, LB_CLEANUP_TIMEOUT, _lb_scroll_cleanup, actor)
                return False
            gActors[aID]['prevPos'] = (event.x, event.y)
            gActors[aID]['prevTime'] = time.time()
            return True
        else:
            print("DBUG:LBMouse:Motion: Stray or Delayed", aID, gLBMMCnt, timeDelta)
            return False
    elif event.type == Clutter.EventType.BUTTON_RELEASE:
        print("DBUG:LBMouse:BtnRelease", aID, gLBMMCnt)
        gActors[aID]['prevPos'] = None
        gActors[aID]['prevTime'] = None
        if gActors[aID]['blur']:
            actor.remove_effect(blurEffect)
            gActors[aID]['blur'] = False
        return Clutter.EVENT_PROPAGATE


def _handle_lb_itemclick(actor, event):
    '''
    This is a indirection to button press handling of listbox items,
    So that the event gets propogated further up the actor hierarchy, in this case upto listbox actor.
    Which inturn ensures that scrolling (by dragging items within the listbox) can be handled.
    '''
    print("lbitemclick")
    handle_itemclick = gActors[actor.get_parent().get_id()]['handle_itemclick']
    if handle_itemclick != None:
        handle_itemclick(actor, event)
    return Clutter.EVENT_PROPAGATE


LB_SELSCALE_PERCENT = 0.1
def create_listbox(posX, posY, sizeX, sizeY, orientation=Clutter.Orientation.HORIZONTAL, iD="listbox", pad=1,
        handle_mouse=_handle_lb_mouse, handle_itemclick=None):
    boxLayout = Clutter.BoxLayout()
    boxLayout.set_orientation(orientation)
    boxLayout.set_spacing(pad)
    boxList = Clutter.ScrollActor()
    if orientation == Clutter.Orientation.HORIZONTAL:
        boxList.set_scroll_mode(Clutter.ScrollMode.HORIZONTALLY)
    elif orientation == Clutter.Orientation.VERTICAL:
        boxList.set_scroll_mode(Clutter.ScrollMode.VERTICALLY)
    #boxList = Clutter.Actor()
    boxList.set_layout_manager(boxLayout)
    boxList.set_id(iD)
    boxList.set_position(posX, posY)
    boxList.set_size(sizeX, sizeY)
    boxList.set_reactive(True)
    gActors[iD] = { 'curIndex': 0,                                  # index to current selection in the listbox
                        'prevPos': None, 'prevTime': None,          # location and time of mouse wrt last event during scroll
                        'posX': 0, 'posY': 0,                       # Corresponds to offset wrt Viewport start
                        'handle_itemclick': handle_itemclick,       # custom handler for handling itemclicks
                        'blur': False }                             # Tell if blur effect is currently active, for example during scroll beyond boundries
    if handle_mouse != None:
        boxList.connect("button-press-event", handle_mouse)
        boxList.connect("button-release-event", handle_mouse)
        boxList.connect("motion-event", handle_mouse)
    return boxList


def listbox_append_child(boxList, childSizeX, childSizeY, childActor, handle_itemclick=None):
    '''
    NOTE: The handle_itemclick passed here should be same as that passed to create_listbox.
    TODO: Verify handle_itemclick passed here matchs one passed to create_listbox.
    TODOAlt: Support seperate handle_itemclick for each individual child.
    '''
    sizeX, sizeY = boxList.get_size()
    orientation = boxList.get_layout_manager().get_orientation()
    if orientation == Clutter.Orientation.HORIZONTAL:
        childActor.set_margin_bottom(sizeY*LB_SELSCALE_PERCENT)
    elif orientation == Clutter.Orientation.VERTICAL:
        childActor.set_margin_right(sizeX*LB_SELSCALE_PERCENT)
    if handle_itemclick != None:
        childActor.connect("button-release-event", _handle_lb_itemclick)
    boxList.add_child(childActor)


def create_listbox_imagebuttons(imageFiles, posX, posY, sizeX, sizeY, btnSizeX, btnSizeY,
        orientation=Clutter.Orientation.HORIZONTAL, iD="listboximagebuttons", pad=1, handle_mouse=_handle_lb_mouse, handle_itemclick=None):
    listBox = create_listbox(posX, posY, sizeX, sizeY, orientation, iD, pad, handle_mouse, handle_itemclick)
    i = 0
    for imageFile in imageFiles:
        btn = create_imagebutton(imageFile, IGNORE, IGNORE, btnSizeX, btnSizeY, "{}.{}".format(iD, i))
        listbox_append_child(listBox, btnSizeX, btnSizeY, btn, handle_itemclick)
        i += 1
    return listBox


AnimOrientation = enum.Flag("AnimOrientation", "BOTH HORIZONTAL VERTICAL")
SelectOffsetType = enum.Flag("SelectOffsetType", "START CUR")
def listbox_select(lb, offset, offsetType=SelectOffsetType.START, animOrientation=None, colorizeEffect=None, scrollToView=True):
    cnt = lb.get_n_children()
    aID = lb.get_id()
    curIndex = gActors[aID]['curIndex']
    if offsetType == SelectOffsetType.CUR:
        nxtIndex = (curIndex + offset) % cnt
    elif offsetType == SelectOffsetType.START:
        nxtIndex = offset % cnt
    #while nxtIndex < 0:
    #    nxtIndex = cnt + nxtIndex
    curActor = lb.get_child_at_index(curIndex)
    nxtActor = lb.get_child_at_index(nxtIndex)
    curActor.save_easing_state()
    nxtActor.save_easing_state()
    lb.save_easing_state()
    lb.set_easing_duration(500)
    if scrollToView:
        nxtActorPos = nxtActor.get_position()
        point = Clutter.Point()
        point.x = nxtActorPos[0]
        point.y = nxtActorPos[1]
        lb.scroll_to_point(point)
    if colorizeEffect != None:
        curActor.remove_effect(colorizeEffect)
    curActor.set_scale(1, 1)
    if (animOrientation == None):
        listOrientation = lb.get_layout_manager().get_orientation()
        if listOrientation == Clutter.Orientation.HORIZONTAL:
            animOrientation = AnimOrientation.VERTICAL
        elif listOrientation == Clutter.Orientation.VERTICAL:
            animOrientation = AnimOrientation.HORIZONTAL
        else:
            print("WARN:animate_listbox:Unknown listbox Orientation")
            animOrientation = AnimOrientation.BOTH
    if (animOrientation == AnimOrientation.HORIZONTAL):
        xScale = 1 + LB_SELSCALE_PERCENT
        yScale = 1
    elif (animOrientation == AnimOrientation.VERTICAL):
        xScale = 1
        yScale = 1 + LB_SELSCALE_PERCENT
    else:
        xScale = 1 + LB_SELSCALE_PERCENT
        yScale = 1 + LB_SELSCALE_PERCENT
    nxtActor.set_scale(xScale, yScale)
    if colorizeEffect != None:
        nxtActor.add_effect(colorizeEffect)
    curActor.restore_easing_state()
    nxtActor.restore_easing_state()
    lb.restore_easing_state()
    gActors[aID]['curIndex'] = nxtIndex


# UI Helpers
def animate_list(lBtns, lPos, iYRotate=0):
    lBtns[lPos].save_easing_state()
    lBtns[lPos].set_scale(1, 1)
    lBtns[lPos].restore_easing_state()
    lPos += 1
    lPos = lPos % len(lBtns)
    lBtns[lPos].save_easing_state()
    #lBtns[lPos].set_scale(1.2, 1)
    lBtns[lPos].set_rotation_angle(Clutter.RotateAxis.Y_AXIS, iYRotate)
    lBtns[lPos].restore_easing_state()
    return lPos, iYRotate


