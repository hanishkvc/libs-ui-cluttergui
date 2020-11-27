#!/usr/bin/env python3
# Generate some test images
# HanishKVC, 2020

import pygame

# Setup a surface
#s=pygame.display.set_mode((640,480))
s=pygame.Surface((128,128))
surfaceSize = s.get_size()


# Get a font
pygame.font.init()
f=pygame.sysfont.SysFont(None,32)


def gen_image(text, fileName):
    s.fill((128,128,128))
    fs=f.render(text, True, (0,0,100))
    textSize = fs.get_size()
    x = (surfaceSize[0] - textSize[0])/2
    y = (surfaceSize[1] - textSize[1])/2
    s.blit(fs,(x,y))
    pygame.image.save(s, fileName)


# What do we want
groups = { "Cat": 5, "Item": 10 }

for g in groups:
    groupMemberCnt = groups[g]
    for i in range(groupMemberCnt):
        text = "{}{}".format(g, i)
        fileName = "{}.png".format(text)
        print(fileName)
        gen_image(text, fileName)

