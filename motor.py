'''
Motor Classes and Methods
'''
import time
import RPi.GPIO as GPIO
import numpy as np

class stepper_motor():
    def __init__(gpiopins, #Enter the pins to be used. The first is the sleep, the rest are Ain1, Ain2, Bin2, Bin1 
                **kwargs):
        if len(gpiopins) != 5:
            raise ValueError('Must Supply 5 gpiopins! The first is the sleep!')
        GPIO.setmode(GPIO.BCM) #We will default to BCM in all of the programs, Do not set mode to GPIO.Board anywhere else in the program!
        self.gpiopins = gpiopins
        
    def __coils__(state):#[a1,a2,b1,b2]
        #A better name for this function would be SetCoilsState() but I was going fast and that was too long
        GPIO.output(self.gpiopins[1],state[0])
        GPIO.output(self.gpiopins[2],state[1])
        GPIO.output(self.gpiopins[3],state[3])#This is tricky: I set pin 23 to state[3]
        GPIO.output(self.gpiopins[4],state[2])#but I set 24 to state [2]. This matches the fact that b2 is closer to a2 than b1 is on the Driver chip.
    
    def turn(turns, #Number of units to turn, if units = 'rev' then this is the number of cycles it makes, if units = 'rad' or 'deg' this is the angle through which it sweeps
            units = 'rev',
            steptype = 'full',
            rpm = 30):
                
        if (steptype != 'full') or (steptype != 'half'):
            raise ValueError('"steptype" must be a string: either "full" or "half"!')
        if (units != 'rev') or (units != 'rad') or (units != 'deg'):
            raise ValueError('"units" must be a string: either "rad" , "rev" , or "deg"')
            
        if rpm < 0 or rpm > 1000:
            raise ValueError('"rpm" must be 0 < rpm < 1000')
        GPIO.setup(self.gpiopins ,GPIO.OUT,initial = 0) #setting up the GPIO pins
        #Slp = 0
        #Ain1 = 1
        #Ain2 = 2
        #Bin2 = 3
        #Bin1 = 4
 
        GPIO.output(self.gpiopins[0],1) #Turns Driver Chip ON by setting self.gpiopins[0] ON

        spr = 200 #Specified by Hardware of NEMA 17 stepper motor
        rpm = 30
        if turns > 0:
            fb = 1 #fb = forward-backward. If you look at the for loops below, in each iteration we add fb, not 1. If fb is -1, we would be adding -1 and so subtracting
            #Subtracting from i means going backward through the states and so fb = 1 is forward, fb = -1 is backwards
        if turns < 0:
            fb = -1
        else:
            raise ValueError("Turns Cannont be Zero")
        
        if units == 'rad':
            turns = turns / (2*np.pi)
        if units == 'deg':
            turns = turns / (360)
        delay = 60 / (spr*rpm) #We get this 
        steps = turns * spr

        if steptype == 'full': #Fullstep
            states = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]
            time.sleep(0.2)

            start = time.perf_counter()
            for i in range(steps):
                i = (i + fb) % 4 #This was too clever to leave out!
                __coils__(states[i*fb])
                time.sleep(delay)

        elif steptype == 'half': #HalfStep
            states = [[1,0,0,0],[1,0,1,0],[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,1,0,1],[0,0,0,1],[1,0,0,1]]
            time.sleep(0.1)

            start = time.perf_counter()
            steps = 2*steps #When we switch to a 8-state cycle, the amount of steps per rotation doubles.
            #for the sake of resuing code, we simply double the steps to compensate.
            for i in range(steps):
                i = (i + fb) % 8 #Notice how now it's 8!
                __coils__(states[i*fb])
                time.sleep(delay)
                
        else:
            print("steptype must be either 'full' or 'half'") #Told you so!

        __coils__([0,0,0,0])
        
class servo():
    def __init__(gpiopins):
        if isinstance(gpiopins, int) is False:
            raise ValueError('servo "gpiopins" is only one number, must be int')
        
        self.gpiopins = gpiopins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpiopins,GPIO.OUT)
        self.pw = GPIO.PWM(self.gpiopins, 50)
        
    def start():
        self.pw.start(7.5)
        
    def set_angle(angle):
        dutycycle = 7.5 + angle*2/30
        self.pw.change(dutycycle)
      
    def stop():
        self.pw.stop()