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

class Calculator(GraphicsEventSystem):

    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        window = self.windowSystem.createWindow(0.1, 0.1, 200, 200, "Magic Calculator")
        window.addWidget(
                self.windowSystem.createButton(0, 0, 30, 30, COLOR_LIGHT_BLUE, title = " 4",value=4, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.04, 0, 30, 30, COLOR_LIGHT_BLUE,title = " 9",value=9, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.08, 0, 30, 30, COLOR_LIGHT_BLUE,title = " 2",value=2, onClick = self.onClick))
        

        window.addWidget(
                self.windowSystem.createButton(0, 0.04, 30, 30, COLOR_LIGHT_BLUE,title = " 3",value=3, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.04, 0.04, 30, 30, COLOR_LIGHT_BLUE,title = " 5",value=5, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.08, 0.04, 30, 30, COLOR_LIGHT_BLUE,title = " 7",value=7, onClick = self.onClick))
        
        window.addWidget(
                self.windowSystem.createButton(0, 0.08, 30, 30, COLOR_LIGHT_BLUE,title = " 8",value=8, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.04, 0.08, 30, 30, COLOR_LIGHT_BLUE,title = " 1",value=1, onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.08, 0.08, 30, 30, COLOR_LIGHT_BLUE,title = " 6",value=6, onClick = self.onClick))
        
        window.addWidget(
                self.windowSystem.createButton(0.13, 0, 30, 30, COLOR_LIGHT_BLUE,"  %", False))
        window.addWidget(
                self.windowSystem.createButton(0.13, 0.04, 30, 30, COLOR_LIGHT_BLUE,"  x", False))
        window.addWidget(
                self.windowSystem.createButton(0.13, 0.08, 30, 30, COLOR_LIGHT_BLUE,"  -",False))

        windowSystem.windowStack.append(window)
        
        self.calculatorStack = []
                
    def onClick(self, widget, window):
        print(widget.value)
        #self.calculatorStack.append