#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Maximilian Röttgen (#332048)
and Carl Orge Retzlaff (#348946)
"""

from GraphicsEventSystem import *
from Window import *

class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.menu = None
        self.menuHeight = 0
        self.titleBarHeight = 20
        self.taskBarHeight = 30
        self.inactiveColor = "#FF00AE"
        self.darkColor = "#2A2D34"
        self.activeColor = "#7EB77F"
        self.white = "#F8F8FF"

    def checkWindowPosition(self, window):
        if (window is -1): return
        frameWidth = self.windowSystem.width
        frameHeight = self.windowSystem.height

        # there is nothing left or above the origin (x,y == 0,0)
        # also there are no relative positions >= 1

        # We will probably need to change this to absolute metrics at some point
        if window.x < 0:
            window.x = 0.001
        elif window.x >= 1:
            window.x = 0.94
        if window.y < 0:
            window.y = 0.05
        elif window.y >= 1:
            window.y = 0.94

    # decorates a standard window
    def decorateWindow(self, window):
        if (window is -1): return
        self.windowSystem.fillRectRelative(window.x, window.y, window.width, -20, self.inactiveColor)

        # close-button
        self.windowSystem.fillRectRelative(window.x, window.y, 20, -20, "#D62839")
        self.windowSystem.drawStringRelative("X", window.x, window.y,self.darkColor, -18,4)

        # minimize-button
        self.windowSystem.fillRectRelative(window.x, window.y, 20, -20, "#BACDB0",0, 20)
        self.windowSystem.drawStringRelative("...", window.x, window.y,self.darkColor, -18,24)

        self.windowSystem.drawStringRelative(window.title, window.x, window.y,self.darkColor, -18, 44)
        self.windowSystem.strokeRectRelative(window.x, window.y, window.width+1, window.height+21, self.darkColor, -21, -1)


    # decorates a focused window
    def decorateFocusedWindow(self, window):
        if (window is -1): return
        self.windowSystem.fillRectRelative(window.x, window.y, window.width, -20, self.activeColor)

        # close-button
        self.windowSystem.fillRectRelative(window.x, window.y, 20, -20, "#D62839")
        self.windowSystem.drawStringRelative("X", window.x, window.y,self.darkColor, -18,4)

        # minimize-button
        self.windowSystem.fillRectRelative(window.x, window.y, 20, -20, "#BACDB0",0, 20)
        self.windowSystem.drawStringRelative("...", window.x, window.y,self.darkColor, -18,24)

        self.windowSystem.drawStringRelative(window.title, window.x, window.y,self.darkColor, -18, 42)
        self.windowSystem.strokeRectRelative(window.x, window.y, window.width+1, window.height+21, self.darkColor, -21, -1)


    def decorateLabel(self, widget,window):
        self.windowSystem.fillRectRelative(widget.x, widget.y, widget.width, -20, self.activeColor, "test")

    #for now only resize of the widgets in their width and height, padding etc propably in next assignment
    def resizeWidget(self, window, widget):

        relWidthChange = window.width/self.oldWidth
        relHeightChange = window.height/self.oldHeight

        widget.x = widget.x*relWidthChange
        widget.y = widget.y*relHeightChange


        relWidgetWidth = widget.width/self.oldWidth

        relWidgetHeight = widget.height/self.oldHeight

        widget.width = relWidgetWidth*window.width
        widget.height = relWidgetHeight*window.height

    def resizeWindow(self, window, x, y):
        self.oldWidth = float(window.width)
        self.oldHeight = float(window.height)

        absXchange = self.windowSystem.downX - x
        absYchange = self.windowSystem.downY - y

        window.width = self.oldWidth-absXchange
        if(window.width <= 10):
            window.width = 10

        window.height = self.oldHeight-absYchange
        if(window.height <= 10):
            window.height = 10

        for widget in window.widgetList:
            self.resizeWidget(window, widget)

        # now we render the newly sorted stack
        self.windowSystem.requestRepaint()

        self.windowSystem.downX = x
        self.windowSystem.downY = y

    # Warum heißt die depressButton? Weil er traurig ist
    # makes the button look pressed when MouseDown occurs on button
    def depressButton(self, widget, window):
        self.windowSystem.fillRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, COLOR_GRAY, 0,0)
        self.windowSystem.strokeRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, COLOR_BLACK, 0,0)
        self.windowSystem.drawStringRelative(widget.title,window.x+widget.x, window.y+widget.y)

    def hoverWidget(self, widget, window):
        self.windowSystem.fillRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, COLOR_GRAY, 0,0)
        self.windowSystem.drawStringRelative(widget.title,window.x+widget.x, window.y+widget.y)


    def drawTaskBar(self):
        x_offset = 0

        # draw the taskbar
        self.windowSystem.fillRectRelative(0, 1, self.windowSystem.width, -self.taskBarHeight, COLOR_GRAY,0,0)

        # draw the menu icon
        self.windowSystem.fillRectRelative(1,1,-20,-self.taskBarHeight,COLOR_BLACK)
        self.windowSystem.drawStringRelative("///",1,1,self.activeColor,-18,-17)

        for window in self.windowSystem.windowList:
            if (self.windowSystem.getTopWindow() is not -1 and window is self.windowSystem.getTopWindow()):
                self.windowSystem.fillRectRelative(0,1,20,-self.taskBarHeight,self.activeColor, 0, x_offset)
                self.windowSystem.drawStringRelative(window.title[0],0,1,self.darkColor, -18, 3+x_offset)

            else:
                self.windowSystem.fillRectRelative(0,1,20,-self.taskBarHeight,self.inactiveColor,0,x_offset)
                self.windowSystem.drawStringRelative(window.title[0],0,1,self.darkColor, -18, 3+x_offset)

            x_offset = x_offset+20

    def startApp(self, widget, window):
        self.windowSystem.openWindow(widget.value.getWindow())

    def shutDown(self,arg1,arg2):
        print("Quitting...")
        quit()

    def toggleMenu(self, isOpen):
        if(isOpen):
            self.menu = None
        else:
            self.menuHeight = (len(self.windowSystem.appList)+1) * 40 + 10
            self.menu = self.windowSystem.createWindow(1,1,-190,-self.menuHeight, "///", COLOR_BLACK)

            y_offset = self.taskBarHeight+40
            for item in self.windowSystem.appList:
                name = item.name
                self.menu.addWidget(self.windowSystem.createButton(0, 0, 170, 30,  self.activeColor,-y_offset, -180, title=" > " + name, value=item, onClick=self.startApp))
                y_offset = y_offset + 40

            self.menu.addWidget(self.windowSystem.createButton(0, 0, 170, 30,  self.inactiveColor,-y_offset, -180, title=" > Power Off", value=item, onClick=self.shutDown))

            self.windowSystem.drawWindow(self.menu, False, -self.taskBarHeight,0)
