#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Maximilian Röttgen (#332048)
and Carl Orge Retzlaff (#348946)
"""
from Window import *
from GraphicsEventSystem import *

class Widget(Window):
    def __init__(self, originX, originY, width, height, title, fillColor, font, hovered = False, y_offset = 0, x_offset=0):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.title = title
        self.fillColor = fillColor
        self.font = font
        self.hovered = hovered
        self.y_offset = y_offset
        self.x_offset = x_offset


class Button(Widget):
    def __init__(self,originX, originY, width, height, fillColor,y_offset=0,x_offset=0, **kwargs):#, title= None, value = None, depressed = False, onClick = None):
        self.depressed = False
        self.value = 0
        self.title = None
        for key in kwargs:
            setattr(self, key, kwargs[key])
        Widget.__init__(self,originX, originY, width, height, self.title, fillColor, "font", False, y_offset, x_offset)

class Slider(Widget):
    def __init__(self,originX, originY, width, height, fillColor,y_offset=0,x_offset=0, **kwargs):
        self.dragged = False
        self.boxPosition = 0
        self.value = 0
        self.title = None
        self.window = False
        for key in kwargs:
            setattr(self, key, kwargs[key])
        Widget.__init__(self,originX, originY, width, height, self.title, fillColor, "font", False, y_offset, x_offset)
