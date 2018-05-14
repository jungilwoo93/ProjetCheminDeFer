# -*- coding: utf-8 -*-
"""
Created on Fri May 11 14:32:38 2018

@author: panpa
"""
"""import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.add_patch(
    patches.Rectangle(
        (0.1, 0.1),   # (x,y)
        0.5,          # width
        0.5,        # height
        fill=False
    )
)
#fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')"""
    
import pygame
#import sys
from pygame.locals import *
    
pygame.init()

white = {255,255,255}
black ={0,0,0}

myScreen=pygame.display.set_mode({1020,800})

#pygame.draw.rect(myScreen,black,{0,0,1020,800})