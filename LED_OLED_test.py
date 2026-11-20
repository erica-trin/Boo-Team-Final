import tkinter as tk
from gpiozero import LED

# Initialize the 3 LEDs using BCM GPIO numbers (NOT physical pin numbers!)
# GPIO 22 = Physical Pin 15
# GPIO 23 = Physical Pin 16
# GPIO 24 = Physical Pin 18
jupiter_led = LED(22)
mars_led = LED(23)
neptune_led = LED(24)

root = tk.Tk()
root.title("Space Tea - LED Test")
root.geometry("480x800")

def select_drink(drink_name):
    # Turn all LEDs off first
    jupiter_led.off()
    mars_led.off()
    neptune_led.off()

    if "Jupiter" in drink_name:
        jupiter_led.on()
        label.config(text="Jupiter LED (GPIO 22) ON", fg="orange")
    elif "Mars" in drink_name:
        mars_led.on()
        label.config(text="Mars LED (GPIO 23) ON", fg="red")
    elif "Neptune" in drink_name:
        neptune_led.on()
        label.config(text="Neptune LED (GPIO 24) ON", fg="blue")

def all_off():
    jupiter_led.off()
    mars_led.off()
    neptune_led.off()
    label.config(text="All LEDs OFF - Tap a drink:", fg="black")

label = tk.Label(root, text="Tap a drink to test its LED:", font=("Arial", 18), justify="center")
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

btn_off = tk.Button(root, text="Turn All LEDs Off", font=("Arial", 12),
                    command=all_off, height=2, width=20)
btn_off.pack(pady=30)

root.mainloop()