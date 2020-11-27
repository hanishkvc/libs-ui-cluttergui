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


# update the surface
s.fill((128,128,128))
text = "testme"
#print(f.size(text))
fs=f.render("testme",True,(0,0,100))
textSize = fs.get_size()
x = (surfaceSize[0] - textSize[0])/2
y = (surfaceSize[1] - textSize[1])/2
s.blit(fs,(x,y))


# Show the surface to user
#pygame.display.update()


# Save the surface for user
pygame.image.save(s,"/tmp/testme.png")

