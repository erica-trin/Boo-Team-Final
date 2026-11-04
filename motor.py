'''
Motor Classes and Methods
'''
import time
import RPi.GPIO as GPIO
import numpy as np

class stepper_motor()
    def __init__(gpiopins, #Enter the pins to be used. The first is the sleep, the rest are Ain1, Ain2, Bin2, Bin1 
                **kwargs):
        if len(gpiopins) != 5
            raise ValueError('Must Supply 5 gpiopins! The first is the sleep!')
        GPIO.setmode(GPIO.BCM) #We will default to BCM in all of the programs, Do not set mode to GPIO.Board anywhere else in the program!
        self.gpiopins = gpiopins
    
    def turn(turns, #Number of units to turn, if units = 'rev' then this is the number of cycles it makes, if units = 'rad' or 'deg' this is the angle through which it sweeps
            units = 'rev')
        steptype = 1 #0 or 1. 0 is a 4 step cycle, 1 is a 8 step cycle. I include both in this program and this variable is how I switch between the two quickly. 
        cl = [17,27,22,23,24] #This is the GPIO BCM # array. 
        #Slp = 17
        #Ain1 = 27
        #Ain2 = 22
        #Bin2 = 23
        #Bin1 = 24

GPIO.setmode(GPIO.BCM) #Did you know BCM is a 18+ website? It's not for the reason you think it is though. 
GPIO.setup(cl,GPIO.OUT,initial = 0) #setting up the GPIO pins

GPIO.output(cl[0],1) #Turns Driver Chip ON by setting GPIO BCM 17 ON

def coils(state):#[a1,a2,b1,b2]
    #A better name for this function would be SetCoilsState() but I was going fast and that was too long
    GPIO.output(cl[1],state[0])
    GPIO.output(cl[2],state[1])
    GPIO.output(cl[3],state[3])#This is tricky: I set pin 23 to state[3]
    GPIO.output(cl[4],state[2])#but I set 24 to state [2]. This matches the fact that b2 is closer to a2 than b1 is on the Driver chip.

spr = 200 #Specified by Hardware
turns = 2
rpm = 30
fb = 1 #fb = forward-backward. If you look at the for loops below, in each iteration we add fb, not 1. If fb is -1, we would be adding -1 and so subtracting
#Subtracting from i means going backward through the states and so fb = 1 is forward, fb = -1 is backwards

delay = 60 / (spr*rpm) #We get this 
steps = turns * spr

if steptype == 0: #Fullstep
    states = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]
    co = states[0] #Artifact from old code, left in because it was there during the lab
    
    time.sleep(0.2)

    start = time.perf_counter()
    for i in range(steps):
        i = (i + fb) % 4 #This was too clever to leave out!
        coils(states[i*fb])
        time.sleep(delay)
    elapsed = time.perf_counter() - start
    print("Time taken =", elapsed)
    print("# Rotations = ", turns)
    print("RPM = ", turns*60/elapsed)
    print("Revolution Period = ", elapsed/turns)
    print("Step Period = ", elapsed/steps)
    print("Step Frequency = ", steps/elapsed)
    print("# Steps = ", steps)
    print("Rotation Angle per Step = ", 360*turns/steps)
elif steptype == 1: #HalfStep
    states = [[1,0,0,0],[1,0,1,0],[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,1,0,1],[0,0,0,1],[1,0,0,1]]
    time.sleep(0.1)

    start = time.perf_counter()
    steps = 2*steps #When we switch to a 8-state cycle, the amount of steps per rotation doubles.
    #for the sake of resuing code, we simply double the steps to compensate.
    for i in range(steps):
        i = (i + fb) % 8 #Notice how now it's 8!
        coils(states[i*fb])
        time.sleep(delay)
    elapsed = time.perf_counter() - start
    print("Time taken =", elapsed)
    print("RPM = ", turns*60/elapsed)
    print("# Rotations = ", turns)
    print("Revolution Period = ", elapsed/turns)
    print("Step Period = ", elapsed/(steps))
    print("Step Frequency = ", steps/elapsed)
    print("# Steps = ", steps)
    print("Rotation Angle per Step = ", 360*turns/steps)
else:
    print("steptype must be either 0 or 1!") #Told you so!

coils([0,0,0,0])
GPIO.cleanup()