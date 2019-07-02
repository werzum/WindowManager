# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:47:12 2019

@author: e.awerg
"""

from GraphicsEventSystem import *
from WindowManager import *
from Window import *
from UITK import *
#from WindowSystem import *

class HelloWorld(GraphicsEventSystem):

    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        window = self.windowSystem.createWindow(0.1, 0.1, 200, 200, "Hello World")
        window.addWidget(
                self.windowSystem.createLabel(0.0175, 0.02, 175, 30, "Please select a language",COLOR_LIGHT_BLUE,"Helvetica", False))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.1, 175, 30, COLOR_LIGHT_BLUE, title=" Deutsch", onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.15, 175, 30, COLOR_LIGHT_BLUE, title=" English", onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.2, 175, 30, COLOR_LIGHT_BLUE, title=" Fran"+u"\u00E7"+"ais", onClick = self.onClick))
        windowSystem.windowStack.append(window)
                
    def onClick(self, widget, window):
        print("called")
        if "Deutsch" in widget.title:
            print("doitrsch")
            window.widgetList[0].title  = " Guten Tag"
        elif "English" in widget.title:
            window.widgetList[0].title  = " Good Morning"
        elif " Fran"+u"\u00E7"+"ais" in widget.title:
            window.widgetList[0].title = "Bonjour"