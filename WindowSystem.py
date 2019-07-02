#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Window System - Submission
by  Maximilian Röttgen (#332048)
and Carl Orge Retzlaff (#348946)
"""

from GraphicsEventSystem import *
from WindowManager import *
from Window import *
from UITK import *
from Apps import *


class WindowSystem(GraphicsEventSystem):

    def start(self):

        self.windowManager = WindowManager(self)
        self.menuOpen = True

        # Created windows are stored in a windowStack
        self.windowStack = []

        self.appList = []
        self.appList.append(HelloWorld(self))
        self.appList.append(Calculator(self))
        self.appList.append(RGBSlider(self))

        self.windowStack.append(
            self.createWindow(0.7, 0.1, 200, 400, "Long window"))
        self.windowStack.append(
            self.createWindow(0.3, 0.3, 200, 200, "Slider Window"))

        self.windowStack[1].addWidget(
            self.createLabel(0.1, 0.05, 100, 50, "Label",COLOR_LIGHT_BLUE,"Helvetica", False))

        self.windowStack[1].addWidget(
            self.createSlider(0.1, 0.2, 100, 20, COLOR_GRAY, onClick = self.uselessFunc, window = False, title = "Testlabel"))
        
        #self.rGBSlider = RGBSlider(self)

        # copy the windowstack to populate our taskbar
        self.windowList = list(self.windowStack)

    # short helper function to return the topmost window (z-level)
    def getTopWindow(self):
        if (len(self.windowStack) > 0):
            return self.windowStack[len(self.windowStack) - 1]
        else:
            return -1

    def uselessFunc(self, widget, window):
        pass
        
    def drawLineRelative(self, x1, y1, x2, y2):

        #converting coordinates to absolute
        x1 = x1 * self.width
        x2 = x2 * self.width
        y1 = y1 * self.height
        y2 = y2 * self.height

        self.setStrokeColor("black")
        self.drawLine(x1, y1, x2, y2)

    # default strokeColor should be the same as windowManager.darkColor
    def fillRectRelative(self, x, y, width, height, fillColor="#2A2D34", y_offset=0, x_offset=0, x_absolute = False):
        #converting coordinates to absolute
        x1 = x * self.width + x_offset
        if x_absolute is True:
            x1 = x
        y1 = y * self.height + y_offset
        x2 = x1 + width
        y2 = y1 + height
        self.setFillColor(fillColor)
        self.fillRect(x1, y1, x2, y2)

    # default strokeColor should be the same as windowManager.darkColor
    def strokeRectRelative(self, x, y, width, height, strokeColor="#2A2D34", y_offset=0, x_offset=0):

        x1 = x * self.width + x_offset  #converting coordinates to absolute
        y1 = y * self.height + y_offset
        x2 = x1 + width
        y2 = y1 + height
        self.setStrokeColor(strokeColor)
        self.strokeRect(x1, y1, x2, y2)

    # default fillColor should be the same as windowManager.darkColor
    def drawStringRelative(self, string, x, y, fillColor="#2A2D34", y_offset=0, x_offset=0):
        x = x * self.width + x_offset  #converting coordinates to absolute
        y = y * self.height + y_offset
        self.setStrokeColor(fillColor)
        self.drawString(string, x, y)


    def handlePaint(self):
        self.drawLineRelative(0.2, 0.3, 0.8, 0.7)

        # draw windows from windowstack and widgets from widgetlist
        #if marked as hovered or depressed draw them differently
        for window in self.windowStack:
            self.drawWindow(window)

        # decorate the focused window (that is on top of the windowStack) differently
        # all windows are decorated with default decorations at creation
        self.windowManager.decorateFocusedWindow(self.getTopWindow())

        self.windowManager.drawTaskBar()
        self.windowManager.toggleMenu(self.menuOpen)


    # default fillColor should be the same as windowManager.white
    def createWindow(self, originX, originY, width, height, title, fillColor="#F8F8FF"):

        window = Window(originX, originY, width, height, title, fillColor)

        return window

    def createLabel(self, originX, originY, width, height, title, fillColor, font, hovered):

        #self.setFont(font)
        widget = Widget(originX, originY, width, height, title, fillColor, font, hovered)

        return widget

    def createButton(self, originX, originY, width, height, fillColor, y_offset=0, x_offset=0, **kwargs):
        button = Button(originX, originY, width, height, fillColor, y_offset,x_offset, **kwargs)

        return button

    def createSlider(self, originX, originY, width, height, fillColor, y_offset=0, x_offset=0, **kwargs):
        slider = Slider(originX, originY, width, height, fillColor, y_offset,x_offset, **kwargs)
        window = slider.window
        print(window)
        if window is False:
            window = self.getTopWindow()
        slider.boxPosition = window.x*self.width+slider.x*self.width+(slider.width/2)
        print(slider.boxPosition)
        
        return slider

    def drawWindow(self, window, decorate=True, y_offset=0, x_offset=0):
        if(decorate): self.windowManager.checkWindowPosition(window)
        self.fillRectRelative(window.x, window.y, window.width, window.height, window.fillColor,y_offset,x_offset)
        if(decorate): self.windowManager.decorateWindow(window)

        for widget in window.widgetList:
            if isinstance(widget, Button):
                if widget.depressed is True:
                    self.windowManager.depressButton(widget,window)
                else:
                    self.drawWidget(widget, window)
            elif isinstance(widget, Slider):
                self.drawWidget(widget,window)
            elif widget.hovered is True:
                self.widgetHover(widget)
            else:
                self.drawWidget(widget,window)

        return window

    
    def drawWidget(self, widget,window):
        if isinstance(widget, Button):
            self.fillRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, widget.fillColor, widget.y_offset,widget.x_offset)
            self.drawStringRelative(widget.title,window.x+widget.x, window.y+widget.y, self.windowManager.darkColor, widget.y_offset,widget.x_offset)
            self.strokeRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, COLOR_BLACK, widget.y_offset,widget.x_offset)
            return widget
        
        if isinstance(widget, Slider):
            #draw the box directly with x-axis mapped to the cursor to avoid complications when calculating back and forth from relative to absolute to relative coordinates
            self.fillRectRelative(widget.boxPosition, window.y+widget.y, widget.width/10, widget.height, widget.fillColor, widget.y_offset-widget.height/2,widget.x_offset, x_absolute = True)
            x2 = window.x+widget.x + float(widget.width)/self.width
            self.drawLineRelative(window.x+widget.x, window.y+widget.y, x2, window.y+widget.y)
            #drawing the slider title scaled to widget height
            self.drawStringRelative(widget.title,window.x+widget.x, window.y+widget.y-widget.height*0.002,self.windowManager.darkColor,widget.y_offset,widget.x_offset)

        else:
            self.fillRectRelative(window.x+widget.x, window.y+widget.y, widget.width, widget.height, widget.fillColor, widget.y_offset,widget.x_offset)
            #font is apparently set globally, how do we just do it locally?
            #self.setFont(widget.font)
            self.drawStringRelative(widget.title,window.x+widget.x, window.y+widget.y,self.windowManager.darkColor,widget.y_offset,widget.x_offset)
            #self.setFont("Default")
            return widget

    # animates the sliding box
    def slideWidget(self, widget, window, x):
        #find mix and max position
        maxSlide = window.x*self.width+widget.x*self.width+widget.width-widget.width/10
        minSlide = window.x*self.width+widget.x*self.width
        
        #check if drag-action was inside bounds
        if x < maxSlide and x > minSlide:
            widget.boxPosition = x
            self.fillRectRelative(x, window.y+widget.y, widget.width/10, widget.height, widget.fillColor, widget.y_offset-widget.height/2,widget.x_offset, x_absolute = True)
        #draw the pretty half-line
        x2 = window.x+widget.x + float(widget.width)/self.width
        self.drawLineRelative(window.x+widget.x, window.y+widget.y, x2, window.y+widget.y)
    

    # transforms the click coordinates into a target - intention tuple
    def identifyEvent(self, x, y):
        # check if click was in taskbar or on the menu-button

        if (x > self.width-20 and y > self.height-30):
            return (-1, "menu")

        # yeah, lots of duplicate code because I tried to be creative with the
        # menu position. RIP code complexity and quality
        # The following if clause is only written to handle the menu
        if (not(self.menuOpen) and self.windowManager.menu is not None):
            menu = self.windowManager.menu
            lx = menu.x * self.width + menu.width
            ly = menu.y * self.height + menu.height

            # move by -30 to accord for task bar height
            if(x > lx and y > ly-30 and y < self.height-30):

                for widget in menu.widgetList:
                    # probably only works for this exact case and is
                    # not very flexible
                    wx = self.width + widget.x_offset
                    wy = self.height + widget.y_offset

                    if (x < wx + widget.width and x > wx):
                        if (y < wy + widget.height and y > wy):
                            return (widget, "menu")

                return(menu, "menu")

        pos = 0
        for window in self.windowList:
            if (y > self.height-30 and x < pos + 20 and x > pos):
                # the window was selected in the taskBar
                return (window, "taskBar")
            else:
                pos = pos + 20
        if(y > self.height-30):
            return (-1, "taskBar")

        # check for each window on stack if mouse coordinates lie inside the windows coordinates
        for window in reversed(self.windowStack):
            lx = window.x * self.width  # calculating absolute x-position
            ly = window.y * self.height  # calculating absolute y-position
            if (x > lx and x < lx + window.width):

                if (y > ly and y < ly + window.height):
                    if (y > ly + window.height - 10 and x > lx + window.width-10):
                        # resize area was clicked
                        return (window, "resize")

                    else:
                        # window was clicked, chek if it was on the widget if window is in front
                        if(not(window is self.getTopWindow())):
                            return (window, "window")
                        else:
                            # only listen to events on focused windows
                            for widget in window.widgetList:
                                wx = widget.x * self.width #calculating widget relative coordinates
                                wy = widget.y * self.height #calculating widget relative coordinates

                                if (x < lx+wx+widget.width and x > lx + wx):
                                    if (y < ly+wy+widget.height and y > ly + wy):
                                        if isinstance(widget, Slider):
                                            return (widget, "slide")
                                        else:
                                            return (widget, "widget")

                elif (y > ly - self.windowManager.titleBarHeight and y < ly):

                    # check if we want to close or minimize
                    if (x > lx and x < lx + 20):
                        return (window, "close")
                    elif (x > lx + 20 and x < lx + 40):
                        return (window, "minimize")

                    # window titlebar was clicked
                    return (window, "titleBar")


        # nothing was clicked
        return (-1, "none")

    def bringWindowToFront(self, window):
        # When a window is brought to front, we "pop" it and move it to the top of the stack
        win = window
        self.windowStack.remove(window)
        self.windowStack.append(win)
        self.windowManager.drawTaskBar()
        # now we render the newly sorted stack
        self.requestRepaint()

    def moveWindow(self, window, x, y):
        lx = window.x * self.width  # calculating absolute x-position
        ly = window.y * self.height  # calculating absolute y-position

        absXchange = self.downX - x
        absYchange = self.downY - y

        window.x = (lx-absXchange)/self.width
        window.y = (ly-absYchange)/self.height

        # now we render the newly arranged windows
        self.requestRepaint()

        self.downX = x
        self.downY = y

    def minimizeWindow(self, window):
        self.windowStack.remove(window)
        self.requestRepaint()

    def closeWindow(self, window):
        self.windowStack.remove(window)
        self.windowList.remove(window)
        self.requestRepaint()

    def openWindow(self, window):
        self.windowStack.append(window)
        self.windowList.append(window)
        self.requestRepaint()

    #when MouseReleased on widget ocurred
    def widgetClicked(self, widget):
        print("doing nothing")

    #when MouseReleased on button ocurred
    def buttonClicked(self, widget):
        window = self.getTopWindow()
        widget.onClick(widget, window)
        #self.helloWorld.clicked(widget, window)
    
    def sliderClicked(self, widget):
        window = self.getTopWindow()
        widget.onClick(widget, window)

    # animates the depressed state of the button on mousePressed
    def buttonDepressed(self, widget):
        window = self.getTopWindow()
        self.windowManager.depressButton(widget, window)
        self.requestRepaint()

    # animates the hovering over widgets (not over button, thats kinda pointless, nobody does that)
    def widgetHover(self, widget):
        window = self.getTopWindow()
        self.windowManager.hoverWidget(widget, window)

    # Register the mouse down event
    def handleMousePressed(self, x, y):
        target, intention = self.identifyEvent(x, y)
        self.downOn = target
        self.clickType = intention
        self.downX = x
        self.downY = y
        print("event",target, intention)

        if(target == self.downOn and intention is "widget" or "menu"):
            print(target, intention)
            if isinstance(target, Button):
                target.depressed = True
                self.requestRepaint()
            if isinstance(target, Slider):
                self.slideWidget(target, self.getTopWindow(), x)

        print("mouse down", self.downOn)
        return (x, y)

    # Handle, when it is a click (release, not press)
    def handleMouseReleased(self, x, y):
        target, intention = self.identifyEvent(x, y)
        print("mouse up", target)
        
        if(target == self.downOn and intention is "taskBar"):
            if(target is not -1):
                if(target not in self.windowStack):
                    self.windowStack.append(target)

                self.bringWindowToFront(target)

        elif(target == -1 and intention is "menu"):
            self.menuOpen = not(self.menuOpen)
        elif(target == self.downOn and intention is "close"):
            self.closeWindow(target)
        elif(target == self.downOn and intention is "minimize"):
            self.minimizeWindow(target)
        elif(target == self.downOn and intention is ("titleBar" or "window")):
            self.bringWindowToFront(target)
        elif(target == self.downOn and intention is "widget" or "menu"):
            if isinstance(target, Button):
                target.depressed = False
                self.buttonClicked(target)
            elif isinstance(target, Slider):
                self.sliderClicked(target)
            else:
                self.widgetClicked(target)

        #elif(target == self.downOn and target is not -1):
        #    self.bringWindowToFront(target)

        self.requestRepaint()
        return (x, y)

    # Handle dragging events
    def handleMouseDragged(self, x, y):

        if self.clickType is "titleBar":
            if(self.downOn is not self.getTopWindow()):
                self.bringWindowToFront(self.downOn)
                print("dragging", self.downOn)

            self.moveWindow(self.downOn, x,y)
            for widget in self.downOn.widgetList:
                if isinstance(widget, Slider):
                    widget.boxPosition = self.downOn.x*self.width+widget.x*self.width+(widget.width/2)

        elif self.clickType is "slide":
            self.slideWidget(self.downOn, self.getTopWindow(),x)
            self.requestRepaint()
            
        elif self.clickType is "resize":
            if(self.downOn is not self.getTopWindow()):
                self.bringWindowToFront(self.downOn)
                print("resizing", self.downOn)
            self.windowManager.resizeWindow(self.downOn, x, y)

    def handleMouseMoved(self, x,y):
        target, intention = self.identifyEvent(x,y)

        if(intention is "widget"):
                target.hovered = True
                self.requestRepaint()
        else:
            for window in self.windowStack:
                for widget in window.widgetList:
                    widget.hovered = False
                    self.requestRepaint()
        self.hoverTarget = target
        self.hoverIntention = intention
        self.hoverX = x
        self.hoverY = y

# Let's start your window system!
w = WindowSystem(800, 700)
w.handlePaint
