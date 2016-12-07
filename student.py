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
    TIME_PER_DEGREE = .007
    TURN_MODIFIER = .5
    TURNSPEED = 195
    RIGHT_SPEED = 185
    LEFT_SPEED = 195
    servo = 100
    #0.0 IS THE HEADING OF THE EXIT, EVERY TURN CHANGES THIS NUMBER
    turn_track = 0.0


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
                "6": ("Second Navigate Method", self.nav2),
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

    def setSpeed(self, l, r):
        set_left_speed(l)
        set_right_speed(r)

    def getSpeed(self):
        return self.speed


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
    #Choose path2 changed wide scan to wider scan from choose path
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



    #Timed Degree Right Turn
    def rightTurn(self, deg):
        # adjust the tracker se we know how many degrees away our exit is
        self.turn_track += deg
        print("the exit is " + str(self.turn_track) + "degrees away.")
        # slow down for more exact turning
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #Do turn stuff
        right_rot()
        # use our experiments to calculate the time needed to turn
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        # return speed to normal cruise speeds
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)

    #Timed Degree Left Turn
    def leftTurn(self, deg):
        #adjust the tracker se we know how many degrees away our exit is
        self.turn_track -= deg
        print("the exit is " + str(self.turn_track) + "degrees away.")
        #slow down for more exact turning
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #Do turn stuff
        left_rot()
        #use our experiments to calculate the time needed to turn
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        #return speed to normal cruise speeds
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)


    def setSpeed(self, left, right):
        print("left speed: " + str(left))
        print("right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)


    # AUTONOMOUS DRIVING
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            #todo
            # loop: check that its clear
            #isClear MVP
            #turn_target = self.kenny()
            if self.isClear():
                # lets go forward a little
                self.testDrive()
            #should I backup?
            self.backUp()
            #if i had to stop, pick a path
            turn_target = self.kenny()
            # a positive turn is right
            if turn_target > 0:
                self.rightTurn(abs(turn_target))

            # negative degrees mean left
            else:
                # let's remove the negative with abs()
                self.leftTurn(abs(turn_target))

    #a different navigation method to try
    def nav2(self):
        while True:
            answer = self.choosePath2()
            if answer == "left":
                #self.leftTurn(90)
                self.leftTurn(turn_target)
            elif answer == "right":
                #self.rightTurn(90)
                self.rightTurn(turn_target)
            else:
                print("cant find path")
                break


    #back up when too close to the wall
    def backUp(self):
        if us_dist(15) < 10:
            print("Too close. Backing up for half a second")
            bwd()
            time.sleep(.5)
            self.stop()

                # replacement turn method. find the best option to turn

    def kenny(self):
        # Activate our scanner!
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        # YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        # YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ###########################
        ######### BUILD THE OPTIONS
        # loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                # YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    # set the counter up again for next time
                    count = 0
                    # add this option to the list
                    option.append(x - 8)


        ####################################
        ############## PICK FROM THE OPTIONS - experimental

                    # The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        # the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption

        #this part of the kenny method was exchanged with what is above
        '''
        #######################################################
        ################ PICK FROM THE OPTIONS
        #######################################################
        bestoption = 90
        winner = 0
        for x in option:
            #skip the filler option
            if not x.__index__() == 0:
                print("Choice # " + str(x.__index__()) + " is @ " + str(x) + " degrees")
                ideal = self.turn_track + self.MIDPOINT
                print("my ideal choice would be " + str(ideal))
                if bestoption > abs(ideal - x):
                    bestoption = abs(ideal - x)
                    winner = x - self.MIDPOINT
        return winner
        '''


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

    #cruise method (replacement test drive method)
    def cruise(self):
        # aim forward
        servo(self.MIDPOINT)
        time.sleep(.05)
        # start moving forward
        fwd()
        # start an infinite loop
        while True:
            # break the loop if the sensor reading is closer than our stop dist
            if us_dist(15) < self.STOP_DIST:
                break
            # break every now and then
            time.sleep(.05)
        # stop if the sensor loop broke
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
