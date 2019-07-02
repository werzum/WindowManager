#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Maximilian Röttgen (#332048)
and Carl Orge Retzlaff (#348946)
"""

from GraphicsEventSystem import *

class Window:
    def __init__(self, originX, originY, width, height, title, fillColor):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.title = title
        self.fillColor = fillColor
        self.widgetList = []

    def addWidget(self,widget):
        self.widgetList.append(widget)
