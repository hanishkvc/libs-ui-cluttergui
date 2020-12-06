#!/usr/bin/env python3
# Generate some test images
# HanishKVC, 2020

import pygame

# Setup a surface
#s=pygame.display.set_mode((640,480))
s128=pygame.Surface((128,128))
s64=pygame.Surface((64,64))


# Get a font
pygame.font.init()
f=pygame.sysfont.SysFont(None,32)


def gen_image(s, text, fileName):
    print(text, fileName)
    surfaceSize = s.get_size()
    s.fill((128,128,128))
    fs=f.render(text, True, (0,0,100))
    textSize = fs.get_size()
    x = (surfaceSize[0] - textSize[0])/2
    y = (surfaceSize[1] - textSize[1])/2
    s.blit(fs,(x,y))
    pygame.image.save(s, fileName)


#### What do we want

# Sample categories and Items

groups = { "Cat": 5, "Item": 20 }

for g in groups:
    groupMemberCnt = groups[g]
    for i in range(groupMemberCnt):
        text = "{}{}".format(g, i)
        fileName = "{}.png".format(text)
        gen_image(s128, text, fileName)

# Media Navigation control

controls = [ "Play", "Pause", "Next", "Prev", "Vol+", "Vol-", "Bri+", "Bri-" ]
for control in controls:
    fileName = control + ".png"
    gen_image(s64, control, fileName)

