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

class Calculator(GraphicsEventSystem):

    #set up a string we use to input all button-clicks and then eval with the built-in python-function
    def __init__(self, windowSystem):
        self.name = "Calculator"
        self.windowSystem = windowSystem
        self.calculatorString= ""
        
    #adding a bunch of buttons for the calculator in a magic square to keep it interesting
    def getWindow(self):
        window = self.windowSystem.createWindow(0.1, 0.1, 161, 170, "Magic Calculator")
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
        self.windowSystem.createButton(0, 0.125, 94, 30, COLOR_LIGHT_BLUE,title = " 0",value=0, onClick = self.onClick))


        window.addWidget(
        self.windowSystem.createButton(0.13, 0, 30, 30, COLOR_LIGHT_BLUE,title = " /",value="/", onClick = self.onClick))
        window.addWidget(
        self.windowSystem.createButton(0.13, 0.04, 30, 30, COLOR_LIGHT_BLUE,title = " X",value="*", onClick = self.onClick))
        window.addWidget(
        self.windowSystem.createButton(0.13, 0.08, 30, 30, COLOR_LIGHT_BLUE,title = " -",value="-", onClick = self.onClick))

        window.addWidget(
        self.windowSystem.createButton(0.162, 0, 30, 30, COLOR_LIGHT_BLUE,title = " +",value="+", onClick = self.onClick))
        window.addWidget(
        self.windowSystem.createButton(0.162, 0.04, 30, 30, COLOR_LIGHT_BLUE,title = " %",value="%", onClick = self.onClick))
        window.addWidget(
        self.windowSystem.createButton(0.162, 0.08, 30, 30, COLOR_LIGHT_BLUE,title = " C",value="C", onClick = self.reset))


        window.addWidget(
        self.windowSystem.createButton(0.13, 0.125, 56, 30, COLOR_LIGHT_BLUE,title = " =",onClick = self.getResult))
        window.addWidget(
        self.windowSystem.createButton(0, 0.174, 94, 30, COLOR_LIGHT_BLUE, title = " Result", value = "Result"))

        return window

    def onClick(self, widget, window):
        print(widget.value)
        self.calculatorString = self.calculatorString + str(widget.value)

    def reset(self, widget, window):
        self.calculatorString = ""
        for widget in window.widgetList:
                if widget.value is "Result":
                    widget.title = " "

    #evaluate the string we pieced together with the built-in eval-function, try and catch for division by zero
    def getResult(self, widget, window):
        print(self.calculatorString)
        try:
            total = str(eval(self.calculatorString))
            for widget in window.widgetList:
                if widget.value is "Result":
                    widget.title = " "+total
            self.calculatorString = total
        except:
            print("noooooo")
            self.reset(widget, window)



class RGBSlider(GraphicsEventSystem):

    def __init__(self, windowSystem):
        #initializing different variables we need to store
        self.name = "RGBSlider"
        self.windowSystem = windowSystem
        self.r = 0
        self.g = 0
        self.b = 0
        #the different positions we need to calculate the 255-RGB value of the cursor in regard to the slider position
        self.diff = 0
        self.xmin = 0
        #window is in order to get the slider boxes to know their place on startup
        self.window = False
        self.hex = '#%02x%02x%02x' % (self.r,self.g,self.b)
        
        #set up the required windows and pass the sliders their parent window
    def getWindow(self):
        window = self.windowSystem.createWindow(0.1, 0.1, 200, 200, "RGBSLider")
        self.window = window
        window.addWidget(
        self.windowSystem.createLabel(0, 0, 75, 200, self.hex, COLOR_GRAY,"Nothing", False))
        window.addWidget(
        self.windowSystem.createSlider(0.1, 0.05, 100, 20, COLOR_GRAY, onClick = self.onClickR, title = "Red", window = self.window))
        window.addWidget(
        self.windowSystem.createSlider(0.1, 0.15, 100, 20, COLOR_GRAY, onClick = self.onClickG, title = "Green", window = self.window))
        window.addWidget(
        self.windowSystem.createSlider(0.1, 0.25, 100, 20, COLOR_GRAY, onClick = self.onClickB, title = "Blue", window = self.window))
        return window

    #different functions for r,g and b, 
    def onClickR(self, widget, window):
        #calc the r-value from 0-255 from the x-position of the cursor and the widget position
        self.xmin = window.x*self.windowSystem.width+widget.x*self.windowSystem.width
        self.diff = widget.boxPosition-self.xmin
        self.diff = (float(self.diff))/widget.width*255
        self.r = round(self.diff)
        #actualize the full hex value and the title and colour of the label to show the change
        self.hex = '#%02x%02x%02x' % (self.r,self.g,self.b)
        window.widgetList[0].fillColor = self.hex
        window.widgetList[0].title = self.hex

    def onClickG(self, widget, window):
        self.xmin = window.x*self.windowSystem.width+widget.x*self.windowSystem.width
        self.diff = widget.boxPosition-self.xmin
        print(self.diff)
        self.diff = (float(self.diff))/widget.width*255
        print(self.r,self.g,self.b)
        print(self.diff)
        self.g = round(self.diff)
        self.hex = '#%02x%02x%02x' % (self.r,self.g,self.b)
        window.widgetList[0].fillColor = self.hex
        window.widgetList[0].title = self.hex


    def onClickB(self, widget, window):
        self.xmin = window.x*self.windowSystem.width+widget.x*self.windowSystem.width
        self.diff = widget.boxPosition-self.xmin
        print(self.diff)
        self.diff = (float(self.diff))/widget.width*255
        print(self.r,self.g,self.b)
        print(self.diff)
        self.b = round(self.diff)
        self.hex = '#%02x%02x%02x' % (self.r,self.g,self.b)
        window.widgetList[0].fillColor = self.hex
        window.widgetList[0].title = self.hex
        print("b ",self.b)
        
class HelloWorld(GraphicsEventSystem):

    def __init__(self, windowSystem):
        self.name = "HelloWorld"
        self.windowSystem = windowSystem

    def getWindow(self):
        window = self.windowSystem.createWindow(0.1, 0.1, 200, 200, "Hello World")
        window.addWidget(
                self.windowSystem.createLabel(0.0175, 0.02, 175, 30, "Please select a language",COLOR_LIGHT_BLUE,"Helvetica", False))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.1, 175, 30, COLOR_LIGHT_BLUE, title=" Deutsch", onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.15, 175, 30, COLOR_LIGHT_BLUE, title=" English", onClick = self.onClick))
        window.addWidget(
                self.windowSystem.createButton(0.0175, 0.2, 175, 30, COLOR_LIGHT_BLUE, title=" Fran"+u"\u00E7"+"ais", onClick = self.onClick))
        return window

    def onClick(self, widget, window):
        print("called")
        if "Deutsch" in widget.title:
            print("doitrsch")
            window.widgetList[0].title  = " Guten Tag"
        elif "English" in widget.title:
            window.widgetList[0].title  = " Good Morning"
        elif " Fran"+u"\u00E7"+"ais" in widget.title:
            window.widgetList[0].title = "Bonjour"
