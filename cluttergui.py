#!/usr/bin/env python3
# Clutter based SIMPLE GUI Library
# HanishKVC, v20201124IST1127
#


import enum
# Import Clutter for use
import gi
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf
from gi.repository import Cogl

# Initialise
pathData = "data/"
Clutter.init()


# data loading helpers
def load_pixbuf(imageFile):
    '''
    create a pixbuf from specified image in the data directory
    '''
    imageFile = "{}/{}".format(pathData, imageFile)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(imageFile)
    return pixbuf


# Widget helpers
gActors = {}
blurEffect = Clutter.BlurEffect()
colorizeEffect1 = Clutter.ColorizeEffect()
colorizeEffect1.set_tint(Clutter.color_from_pixel(0xE0E0F0FF))
print(colorizeEffect1.get_tint().to_string())


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


def create_image(imageFile):
    pixbuf = load_pixbuf(imageFile)
    image = Clutter.Image()
    pixelFormat = Cogl.PixelFormat.RGB_888
    if pixbuf.get_has_alpha():
        pixelFormat = Cogl.PixelFormat.RGBA_8888
    image.set_data(pixbuf.get_pixels(), pixelFormat, pixbuf.get_width(), pixbuf.get_height(), pixbuf.get_rowstride())
    return image


def create_imagebutton(imageFile, posX, posY, sizeX, sizeY, id="imagebutton"):
    btnImage = create_image(imageFile)
    imgBtn = Clutter.Actor()
    imgBtn.set_id(id)
    imgBtn.set_content(btnImage)
    imgBtn.set_content_scaling_filters(Clutter.ScalingFilter.LINEAR, Clutter.ScalingFilter.LINEAR)
    imgBtn.set_content_gravity(Clutter.Gravity.CENTER)
    if (posX != -1) and (posY != -1):
        imgBtn.set_position(posX, posY)
    if (sizeX != -1) and (sizeY != -1):
        imgBtn.set_size(sizeX, sizeY)
    imgBtn.set_reactive(True)
    return imgBtn


GESTURE_DELTATIME_MS = 500
def _handle_lb_mouse(actor, event):
    #print("INFO:LbMouse:{}:{}:{},{}:{}".format(event.time, actor, event.x, event.y, event.type))
    aID = actor.get_id()
    if event.type == Clutter.EventType.BUTTON_PRESS:
        gActors[aID]['prevPos'] = (event.x, event.y)
        gActors[aID]['prevTime'] = event.time
        return Clutter.EVENT_STOP
    elif event.type == Clutter.EventType.MOTION:
        prevPos = gActors[aID]['prevPos']
        prevTime = gActors[aID]['prevTime']
        x = gActors[aID]['posX']
        y = gActors[aID]['posY']
        if (prevTime != None) and ((event.time - prevTime) < GESTURE_DELTATIME_MS):
            xD = event.x - prevPos[0]
            yD = event.y - prevPos[1]
            if abs(xD) > abs(yD):
                x -= xD
            else:
                y -= yD
            if (x >= 0) and (y >= 0):
                point = Clutter.Point()
                point.x = x
                point.y = y
                actor.scroll_to_point(point)
                gActors[aID]['posX'] = x
                gActors[aID]['posY'] = y
            else:
                print(x,y)
                if gActors[aID]['blur'] == False:
                    actor.add_effect(blurEffect)
                    gActors[aID]['blur'] = True
            gActors[aID]['prevPos'] = (event.x, event.y)
            gActors[aID]['prevTime'] = event.time
            return True
    elif event.type == Clutter.EventType.BUTTON_RELEASE:
        print("DBUG:LBMouse:BtnRelease")
        gActors[aID]['prevPos'] = None
        gActors[aID]['prevTime'] = None
        if gActors[aID]['blur']:
            actor.remove_effect(blurEffect)
            gActors[aID]['blur'] = False
        return Clutter.EVENT_STOP


def _handle_lb_itemclick(actor, event):
    handle_itemclick = gActors[actor.get_parent().get_id()]['handle_itemclick']
    if handle_itemclick != None:
        handle_itemclick(actor, event)
    return Clutter.EVENT_PROPAGATE


def create_listbox_imagebuttons(imageFiles, posX, posY, sizeX, sizeY, btnSizeX, btnSizeY,
        orientation=Clutter.Orientation.HORIZONTAL, id="listboximagebuttons", pad=1, handle_mouse=_handle_lb_mouse, handle_itemclick=None):
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
    boxList.set_id(id)
    boxList.set_position(posX, posY)
    boxList.set_size(sizeX, sizeY)
    i = 0
    for imageFile in imageFiles:
        btn = create_imagebutton(imageFile, -1, -1, btnSizeX, btnSizeY, "{}.{}".format(id, i))
        if handle_itemclick != None:
            btn.connect("button-release-event", _handle_lb_itemclick)
        boxList.add_child(btn)
        i += 1
    boxList.set_reactive(True)
    gActors[id] = { 'curIndex': 0,                                  # index to current selection in the listbox
                        'prevPos': None, 'prevTime': None,          # location and time of mouse wrt last event during scroll
                        'posX': 0, 'posY': 0,                       # Corresponds to offset wrt Viewport start
                        'handle_itemclick': handle_itemclick,       # custom handler for handling itemclicks
                        'blur': False }                             # Tell if blur effect is currently active, for example during scroll beyond boundries
    if handle_mouse != None:
        boxList.connect("button-press-event", handle_mouse)
        boxList.connect("button-release-event", handle_mouse)
        boxList.connect("motion-event", handle_mouse)
    ''' Trying to get the actual size accounting for all the children and their sizes. Didnt help.
        Nor did I get the actual visible size. Need to look at doc/code of clutter later.
        Maybe from within a paint/draw event, one can get these.
        Dont see why it is not maintained somewhere by the actor. Or else one will have to use
        Stage.size - actor.pos for visible size and lastchild.pos+lastchild.size for actual size.
    print("INFO:CreateListBoxImgBtns:{}:{}:{}:{}:{}".format(boxList.get_size(), boxList.get_clip(),
                boxList.get_allocation_box().get_size(), boxList.get_content_box().get_size(), boxList.get_preferred_size()))
                #boxList.get_paint_box()[1].get_size(), boxList.get_content_box().get_size(), boxList.get_transformed_size()))
    '''
    return boxList


# UI Helper
def animate_list(lBtns, lPos, iYRotate=0):
    lBtns[lPos].save_easing_state()
    lBtns[lPos].set_scale(1, 1)
    lBtns[lPos].restore_easing_state()
    lPos += 1
    lPos = lPos % len(lBtns)
    lBtns[lPos].save_easing_state()
    lBtns[lPos].set_scale(1.2, 1)
    lBtns[lPos].set_rotation_angle(Clutter.RotateAxis.Y_AXIS, iYRotate)
    lBtns[lPos].restore_easing_state()
    return lPos, iYRotate


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
        xScale = 1.1
        yScale = 1
    elif (animOrientation == AnimOrientation.VERTICAL):
        xScale = 1
        yScale = 1.1
    else:
        xScale = 1.1
        yScale = 1.1
    nxtActor.set_scale(xScale, yScale)
    if colorizeEffect != None:
        nxtActor.add_effect(colorizeEffect)
    curActor.restore_easing_state()
    nxtActor.restore_easing_state()
    lb.restore_easing_state()
    gActors[aID]['curIndex'] = nxtIndex


