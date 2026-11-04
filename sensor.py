'''
Sensor Classes and Methods
'''
import time
import RPi.GPIO as GPIO
import numpy as np

class rangefinder(gpiopins)
    def __init__(gpiopins):
        if len(gpiopins) != 5:
            raise ValueError('Must Supply 2 gpiopins!')
        self.gpiopins = gpiopins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpiopins,GPIO.OUT)
        GPIO.setup(self.gpiopins[0], GPIO.OUT, initial=0)
        GPIO.setup(self.gpiopins[1], GPIO.IN)

    def getrange(temp = 20):
        GPIO.output(self.gpiopins[0], 1)
        time.sleep(10e-6)
        GPIO.output(self.gpiopins[0], 0)
        GPIO.wait_for_edge(self.gpiopins[1],GPIO.RISING)
        t = time.perf_counter()
        GPIO.wait_for_edge(self.gpiopins[1],GPIO.FALLING, timeout=300)
        dt =  time.perf_counter() - t)
        speedofsound = 331.1*np.sqrt(1+temp/273.15)
        return dt*speedofsound/2