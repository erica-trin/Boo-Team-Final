import time
import tkinter as tk
from gpiozero import LED, OutputDevice, DigitalInputDevice

# Initialize the Sensor (using BCM Pin 25)
# active_low=True is common for IR sensors when an object blocks the beam
person_sensor = DigitalInputDevice(25, pull_up=True)

# Initialize the 3 LEDs
jupiter_led = LED(22)
mars_led = LED(23)
neptune_led = LED(24)

# Initialize 3 Pump Relays
jupiter_pump = OutputDevice(17, active_high=False, initial_value=False)
mars_pump = OutputDevice(27, active_high=False, initial_value=False)
neptune_pump = OutputDevice(5, active_high=False, initial_value=False)

# the main window for the display
root = tk.Tk()
root.title("Space Tea")
root.geometry("480x800")

# is someone present?
person_detected = False

def check_sensor():
    global person_detected
    # Read the sensor (if active_low, value is 0 when object is present)
    if person_sensor.is_active: # Person detected
        if not person_detected:
            person_detected = True
            label.config(text="Person Detected! Select Your Drink:", fg="green")
    else:
        if person_detected:
            person_detected = False
            label.config(text="Please wave in front of the sensor", fg="red")
            
    # Run this check again after 100 milliseconds (0.1 seconds)
    root.after(100, check_sensor)

def select_drink(drink_name):
    # Reset state
    jupiter_led.off()
    mars_led.off()
    neptune_led.off()
    jupiter_pump.off()
    mars_pump.off()
    neptune_pump.off()

    # hardware based on selection
    if "Jupiter" in drink_name:
        jupiter_led.on()
        label.config(text=f"Dispensing Jupiter (Mango)...")
        root.update()
        jupiter_pump.on()
        time.sleep(3)
        jupiter_pump.off()

    elif "Mars" in drink_name:
        mars_led.on()
        label.config(text=f"Dispensing Mars (Strawberry)...")
        root.update()
        mars_pump.on()
        time.sleep(3)
        mars_pump.off()

    elif "Neptune" in drink_name:
        neptune_led.on()
        label.config(text=f"Dispensing Neptune (Blueberry)...")
        root.update()
        neptune_pump.on()
        time.sleep(3)
        neptune_pump.off()

    label.config(text=f"Drink poured! Next steps loading... {drink_name}!")

# Title / Status Label at the top
label = tk.Label(root, text="Waiting for person!", font=("Arial", 18), fg="red", justify="center")
label.pack(pady=40)

# Drink Selection Buttons
btn_jupiter = tk.Button(root, text="Jupiter (Mango)", font=("Arial", 14), 
                        command=lambda: select_drink("Jupiter (Mango)"), height=2, width=20, bg="#ffaa55")
btn_jupiter.pack(pady=15)

btn_mars = tk.Button(root, text="Mars (Strawberry)", font=("Arial", 14), 
                     command=lambda: select_drink("Mars (Strawberry)"), height=2, width=20, bg="#ff5555")
btn_mars.pack(pady=15)

btn_neptune = tk.Button(root, text="Neptune (Blueberry)", font=("Arial", 14), 
                        command=lambda: select_drink("Neptune (Blueberry)"), height=2, width=20, bg="#55aaff")
btn_neptune.pack(pady=15)

# Start the background sensor check loop as soon as the app launches
root.after(100, check_sensor)

# Run the application window loop
root.mainloop()