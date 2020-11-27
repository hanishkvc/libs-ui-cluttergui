#!/usr/bin/env python3
# Generate some test images
# HanishKVC, 2020

import pygame

# Setup a surface
#s=pygame.display.set_mode((640,480))
s=pygame.Surface((128,128))

# Get a font
pygame.font.init()
f=pygame.sysfont.SysFont(None,32)

# update the surface
s.fill((128,128,128))
text = "testme"
print(f.size(text))
fs=f.render("testme",True,(0,0,100))
print(fs.get_size())
s.blit(fs,(20,20))

# Show the surface to user
#pygame.display.update()

# Save the surface for user
pygame.image.save(s,"/tmp/testme.png")

