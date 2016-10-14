import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 100
    STOP_DIST = 20

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "s": ("check status", self.status),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        print('is it safe to dance?')
        x = 100
        while self.completeClear() and x <= 200:
            print('speed is set to:' + str(x))
            servo(30)
            set_speed(x)
            self.encB(10)
            self.encR(16)
            servo(150)
            servo(30)
            self.encL(32)
            self.encF(7)
            servo(100)
            self.encR(8)
            self.encF(15)
            servo(160)
            time.sleep(.1)
            x += 25


    # Complete Clear Check
    def completeClear(self):
        t=8.5
        print("let's check 0 degrees")
        if not self.isClear():
            return False
        self.encR(t)
        print("let's check 90 degrees")
        if not self.isClear():
            return False
        self.encR(t)
        print("let's check 180 degrees")
        if not self.isClear():
            return False
        self.encR(t)
        print("let's check 270 degrees")
        if not self.isClear():
            return False
        self.encR(t)
        return True





    def status(self):
        print("My power is at "+ str(volt()) +"volts")
        self.encF(9)


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
