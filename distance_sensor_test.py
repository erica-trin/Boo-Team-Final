import threading
import time
import tkinter as tk
import lgpio
from gpiozero import LED

# HC-SR04 Pins (BCM numbering)
TRIG_PIN = 25  # Physical Pin 22
ECHO_PIN = 17  # Physical Pin 11 (from 1k/2k divider)

# Open GPIO chip for the ultrasonic sensor
chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(chip, TRIG_PIN)
lgpio.gpio_claim_input(chip, ECHO_PIN)

# Initialize the 3 Drink LEDs via MOSFET Gates
jupiter_led = LED(22)   # Physical Pin 15
mars_led = LED(23)      # Physical Pin 16
neptune_led = LED(24)   # Physical Pin 18

root = tk.Tk()
root.title("Space Tea")
root.geometry("480x800")

person_detected = False
latest_distance_cm = 999.0
running = True

def read_hcsr04_cm():
    lgpio.gpio_write(chip, TRIG_PIN, 0)
    time.sleep(0.000002)
    lgpio.gpio_write(chip, TRIG_PIN, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(chip, TRIG_PIN, 0)

    timeout = time.time() + 0.04
    while lgpio.gpio_read(chip, ECHO_PIN) == 0:
        if time.time() > timeout:
            return 999.0  # No echo received

    pulse_start = time.time()
    timeout = time.time() + 0.04
    while lgpio.gpio_read(chip, ECHO_PIN) == 1:
        if time.time() > timeout:
            return 999.0

    pulse_end = time.time()
    return (pulse_end - pulse_start) * 17150

def sensor_worker():
    global latest_distance_cm
    while running:
        dist = read_hcsr04_cm()
        latest_distance_cm = dist
        if dist >= 999.0:
            print("Sensor: No echo (check 4.5V battery & shared GND)")
        else:
            print(f"Sensor: {dist:.1f} cm")
        time.sleep(0.2)

def update_ui():
    global person_detected
    if not running:
        return

    if latest_distance_cm < 35:
        label.config(text=f"Person Detected ({latest_distance_cm:.0f} cm)!\nSelect Your Drink:", fg="green")
        person_detected = True
    else:
        if person_detected:
            person_detected = False
            label.config(text="Please step closer to the sensor", fg="red")

    root.after(150, update_ui)

def reset_leds():
    jupiter_led.off()
    mars_led.off()
    neptune_led.off()
    label.config(text="Drink poured! Ready for next order.", fg="black")

def select_drink(drink_name):
    jupiter_led.off()
    mars_led.off()
    neptune_led.off()

    if "Jupiter" in drink_name:
        jupiter_led.on()
        label.config(text="Dispensing Jupiter (Mango)...", fg="orange")
    elif "Mars" in drink_name:
        mars_led.on()
        label.config(text="Dispensing Mars (Strawberry)...", fg="red")
    elif "Neptune" in drink_name:
        neptune_led.on()
        label.config(text="Dispensing Neptune (Blueberry)...", fg="blue")

    root.after(3000, reset_leds)

def on_closing():
    global running
    running = False
    time.sleep(0.25)
    lgpio.gpiochip_close(chip)
    jupiter_led.close()
    mars_led.close()
    neptune_led.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

label = tk.Label(root, text="Waiting for person...", font=("Arial", 18), fg="red", justify="center")
label.pack(pady=40)

btn_jupiter = tk.Button(root, text="Jupiter (Mango)", font=("Arial", 14),
                        command=lambda: select_drink("Jupiter (Mango)"), height=2, width=20, bg="#ffaa55")
btn_jupiter.pack(pady=15)

btn_mars = tk.Button(root, text="Mars (Strawberry)", font=("Arial", 14),
                     command=lambda: select_drink("Mars (Strawberry)"), height=2, width=20, bg="#ff5555")
btn_mars.pack(pady=15)

btn_neptune = tk.Button(root, text="Neptune (Blueberry)", font=("Arial", 14),
                        command=lambda: select_drink("Neptune (Blueberry)"), height=2, width=20, bg="#55aaff")
btn_neptune.pack(pady=15)

root.update_idletasks()
threading.Thread(target=sensor_worker, daemon=True).start()
root.after(200, update_ui)
root.mainloop()