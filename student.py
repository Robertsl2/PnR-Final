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
    TURNSPEED = 195
    RIGHT_SPEED = 185
    LEFT_SPEED = 195
    servo = 100

    def setSpeed(self, l, r):
        set_left_speed(l)
        set_right_speed(r)

    def getSpeed(self):
        return self.speed

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
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
                "5": ("test drive", self.testDrive),
                "s": ("check status", self.status),
                "q": ("Quit", quit)

                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def turnR(self, x):
        previous = self.getSpeed()
        self.setSpeed(self.TURNSPEED)
        self.encR(x)
        self.setSpeed(previous)

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        print('is it safe to dance?')
        x = 100
        while self.completeClear() and x <= 200:
            print('speed is set to:' + str(x))
            servo(30)
            self.setSpeed(x, x-10)
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

    #changed isClear method called moreClear
    def moreClear(self) -> bool:
        for x in range((self.MIDPOINT - 50), (self.MIDPOINT + 50), +30):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            time.sleep(.1)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True

    # Complete Clear Check
    def completeClear(self):
        t=10
        print("let's check 0 degrees")
        if not self.isClear():
            return False
        self.turnR(t)
        print("let's check 90 degrees")
        if not self.isClear():
            return False
        self.turnR(t)
        print("let's check 180 degrees")
        if not self.isClear():
            return False
        self.turnR(t)
        print("let's check 270 degrees")
        if not self.isClear():
            return False
        self.turnR(t)
        return True

    def status(self):
        print("My power is at "+ str(volt()) +"volts")

    def widerScan(self):
        # dump all values
        self.flushScan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)

            # DECIDE WHICH WAY TO TURN

    def choosePath2(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.widerScan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        while True:
            # loop: check that its clear
            #isClear MVP
            while self.moreClear():
                # lets go forward a little
                self.testDrive()
            answer = self.choosePath2()
            if answer == "left":
                self.encL(4)
            elif answer == "right":
                self.encR(4)

    ###Test Drive Method
    def testDrive(self):
        servo(100)
        ###################Change choose path servo speed!!!!!!!!!!
        print("here we go!!")
        fwd()
        while True:
            if us_dist(15) < self.STOP_DIST:
                print("AAAAHHHH! ALL STOP!")
                break
            time.sleep(.05)
            print("Seems clear, keep rolling")
        self.stop()

        ####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
