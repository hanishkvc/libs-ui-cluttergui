#!/usr/bin/env python3
# Test Clutter
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
def handle_lb_mouse(actor, event):
    #print("INFO:LbMouse:{}:{}:{},{}:{}".format(event.time, actor, event.x, event.y, event.type))
    aID = actor.get_id()
    if event.type == Clutter.EventType.BUTTON_PRESS:
        gActors[aID]['prevPos'] = (event.x, event.y)
        gActors[aID]['prevTime'] = event.time
        return Clutter.EVENT_STOP
    elif event.type == Clutter.EventType.MOTION:
        prevPos = gActors[aID]['prevPos']
        prevTime = gActors[aID]['prevTime']
        if (prevTime != None) and ((event.time - prevTime) < GESTURE_DELTATIME_MS):
            xD = event.x - prevPos[0]
            yD = event.y - prevPos[1]
            if abs(xD) > abs(yD):
                gActors[aID]['posX'] -= xD
            else:
                gActors[aID]['posY'] -= yD
            point = Clutter.Point()
            point.x = gActors[aID]['posX']
            point.y = gActors[aID]['posY']
            actor.scroll_to_point(point)
            gActors[aID]['prevPos'] = (event.x, event.y)
            gActors[aID]['prevTime'] = event.time
            return True
    elif event.type == Clutter.EventType.BUTTON_RELEASE:
        print("DBUG:LBMouse:BtnRelease")
        gActors[aID]['prevPos'] = None
        gActors[aID]['prevTime'] = None
        return Clutter.EVENT_STOP


def handle_lb_itemclick(actor, event):
    handle_itemclick = gActors[actor.get_id()]['handle_itemclick']
    if handle_itemclick != None:
        handle_itemclick(actor, event)
    return Clutter.EVENT_PROPAGATE


def create_listbox_imagebuttons(imageFiles, posX, posY, sizeX, sizeY, btnSizeX, btnSizeY,
        orientation=Clutter.Orientation.HORIZONTAL, id="listboximagebuttons", pad=1, handle_mouse=handle_lb_mouse, handle_itemclick=None):
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
            btn.connect("button-release-event", handle_lb_itemclick)
        boxList.add_child(btn)
        i += 1
    boxList.set_reactive(True)
    gActors[id] = { 'curIndex': 0, 'prevPos': None, 'prevTime': None, 'posX': 0, 'posY': 0, 'handle_itemclick': handle_itemclick }
    if handle_mouse != None:
        boxList.connect("button-press-event", handle_mouse)
        boxList.connect("button-release-event", handle_mouse)
        boxList.connect("motion-event", handle_mouse)
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
def animate_listbox(lb, lbPos, animOrientation=None):
    cnt = lb.get_n_children()
    lbNxt = (lbPos + 1) % cnt
    curActor = lb.get_child_at_index(lbPos)
    nxtActor = lb.get_child_at_index(lbNxt)
    curActor.save_easing_state()
    nxtActor.save_easing_state()
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
    curActor.restore_easing_state()
    nxtActor.restore_easing_state()
    return lbNxt


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
    global boxvPos, boxhPos, lPos, lYRotate
    print("INFO:KeyPress:{}:{}:{}".format(actor, event.keyval, chr(event.keyval)), event.flags, event.type, event.modifier_state)
    CMDKEY_MODSTATE = (Clutter.ModifierType.SHIFT_MASK | Clutter.ModifierType.CONTROL_MASK)
    if ((event.modifier_state & CMDKEY_MODSTATE) == CMDKEY_MODSTATE):
        if (event.keyval == Clutter.KEY_A):
            lPos, lYRotate = animate_list(listBtns, lPos, lYRotate+10)
            boxvPos = animate_listbox(boxv, boxvPos)
            boxhPos = animate_listbox(boxh, boxhPos)
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
boxvPos = 0
stage.add_child(boxv)
# Overwriting/Reusing the boxh below, so only the last listbox will be animated
images = [ "Item1.png", "Item2.png", "Item3.png", "Item4.png", "Item5.png", "Item6.png", "Item7.png" ]
boxh = create_listbox_imagebuttons(images, 132,100, 128*6,128, 128,128, Clutter.Orientation.HORIZONTAL, id="il1", handle_itemclick=handle_lb_itemclick)
boxhPos = 0
stage.add_child(boxh)
boxh = create_listbox_imagebuttons(images, 132,240, 128*6,32, 128,128, Clutter.Orientation.HORIZONTAL, id="il2", handle_itemclick=handle_lb_itemclick)
stage.add_child(boxh)
images = [ "Item11.png", "Item12.png", "Item13.png", "Item14.png", "Item15.png", "Item16.png", "Item17.png" ]
boxh = create_listbox_imagebuttons(images, 132,284, 128*6,128, 128,128, Clutter.Orientation.HORIZONTAL)
boxhPos = 0
stage.add_child(boxh)


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
#stage.connect("button-press-event", handle_btn_press)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


