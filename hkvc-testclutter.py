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


# Create the stage
stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Red")[1])
stage.set_size(800,600)
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
    btnPixbuf = load_pixbuf(imageFile)
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


def create_listbox_imagebuttons(imageFiles, posX, posY, sizeX, sizeY, btnSizeX, btnSizeY, orientation=Clutter.Orientation.HORIZONTAL, id="listimagebuttons"):
    boxLayout = Clutter.BoxLayout()
    boxLayout.set_orientation(orientation)
    boxList = Clutter.Actor()
    boxList.set_layout_manager(boxLayout)
    boxList.set_id(id)
    boxList.set_position(posX, posY)
    boxList.set_size(sizeX, sizeY)
    i = 0
    for imageFile in imageFiles:
        x = posX
        y = posY
        if orientation == Clutter.Orientation.HORIZONTAL:
            x = posX + i*btnSizeX
        else:
            x = posX
        if orientation == Clutter.Orientation.VERTICAL:
            y = posY + i*btnSizeY
        else:
            y = posY
        btn = create_imagebutton(imageFile, x, y, btnSizeX, btnSizeY, "{}.{}".format(id, i))
        boxList.add_child(btn)
        i += 1
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
boxv = create_listbox_imagebuttons(images, 2,2, 128,128*4, 128,128, Clutter.Orientation.VERTICAL)
boxv.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, 40)
boxvPos = 0
stage.add_child(boxv)
images = [ "Item1.png", "Item2.png", "Item3.png", "Item4.png", "Item5.png", "Item6.png", "Item7.png" ]
boxh = create_listbox_imagebuttons(images, 140,100, 128*4,128, 128,128, Clutter.Orientation.HORIZONTAL)
boxhPos = 0
stage.add_child(boxh)
images = [ "Item11.png", "Item12.png", "Item13.png", "Item14.png", "Item15.png", "Item16.png", "Item17.png" ]
boxh = create_listbox_imagebuttons(images, 140,300, 128*4,128, 128,128, Clutter.Orientation.HORIZONTAL)
boxhPos = 0
stage.add_child(boxh)


# Get ready to start
print(stage.get_children())
stage.connect("destroy", handle_destroy)
stage.connect("button-press-event", handle_btn_press)
stage.connect("key-press-event", handle_key_press)
stage.show()
Clutter.main()


