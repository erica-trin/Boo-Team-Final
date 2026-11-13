
import time
import tkinter as tk
from gpiozero import LED, OutputDevice, DigitalInputDevice
from motor import stepper_motor, servo
from OLED_code import check_sensor
from ADC3008_SPI import read_adc 

stepper_turntable = stepper_motor([12, 16, 20, 21, 26])

ice_servo = servo(18) #GPIO pin for ice trapdoor servo 
pearl_servo = servo(19) # GPIO pin for pearl trapdoor servo
seal_servo = servo(13) # GPIO pin for sealing arm servo 

# intialize sugar pump (sugar) and stirrer (DC motor)
sugar_pump = OutputDevice(6, active_high=False, initial_value = False)
stir_motor = OutputDevice(11, active_high=False, initial_value=False)
 
def boba_pipeline(chosen_drink, jupiter_pump, mars_pump, neptune_pump, label, root):
    # station 1, liquid 
    label.config(text=f"Station 1: pouring {chosen_drink}...")
    root.update()
    if "Jupiter" in chosen_drink:
        jupiter_pump.on()
        time.sleep(3)
        jupiter_pump.off()
    elif "Mars" in chosen_drink:
        mars_pump.on()
        time.sleep(3)
        mars_pump.off()
    elif "Neptune" in chosen_drink:
        neptune_pump.on()
        time.sleep(3)
        neptune_pump.off()

    # station 2, index & sugar 
    label.config(text="Station 2: adding custom sugar amount...")
    root.update()
    # read pot on ADC channel 0 for dynamic sugar amount
    raw_sugar = read_adc(0)
    sugar_runtime = (raw_sugar / 1023.0) * 4.0 
    sugar_pump.on()
    time.sleep(sugar_runtime)
    sugar_pump.off()
    # run pump 4 for sugar_runtime 
    stepper_turntable.turn(90, units = 'deg', steptype = 'full', rpm = 30) # rotate to next station

    # station 3, ice and pearls 
    label.config(text="Station 3: dispensing ice and pearls...")
    root.update()
    # read second pot for ice on ADC channel 1
    raw_ice = read_adc(1)
    ice_open_time = (raw_ice / 1023.0) * 3.0 

    # open ice trapdoor servo 
    ice_servo.start()
    time.sleep(ice_open_time)
    ice_servo.stop()

    # drop fixed amount of pearls 
    pearl_servo.start()
    time.sleep(1.5) # fixed time for pearls
    pearl_servo.stop()

    stepper_turntable.turn(90, units='deg', steptype = 'full', rpm=30) # rotate to final station 

    # station 4, stir and seal 
    label.config(text="Station 4: stirring & sealing...")
    # turn on DC motor stir stick, then engage sealer servo 
    root.update()
    # turn on DC stir motor 
    stir_motor.on()
    time.sleep(3)
    stir_motor.off()

    # engage sealing servo arm 
    seal_servo.start()
    time.sleep(2)
    seal_servo.stop()

    label.config(text="Order ready! Good luck with your mission!")
    root.update()

