import tkinter as tk

# Main window setup (matching your 480x800 display dimensions)
root = tk.Tk()
root.title("Space Tea - Menu Test")[cite: 3]
root.geometry("480x800")[cite: 3]

def test_select(drink_name):
    # Updates the on-screen text when a button is tapped without touching any GPIO pins
    label.config(text=f"Selected: {drink_name}!\n(Display Test Successful)", fg="green")

# Title / Status Label at the top
label = tk.Label(root, text="Space Tea Menu Test\nTap a drink below:", font=("Arial", 18), fg="blue", justify="center")[cite: 3]
label.pack(pady=40)[cite: 3]

# Drink Selection Buttons[cite: 3]
btn_jupiter = tk.Button(root, text="Jupiter (Mango)", font=("Arial", 14), 
                        command=lambda: test_select("Jupiter (Mango)"), height=2, width=20, bg="#ffaa55")[cite: 3]
btn_jupiter.pack(pady=15)[cite: 3]

btn_mars = tk.Button(root, text="Mars (Strawberry)", font=("Arial", 14), 
                     command=lambda: test_select("Mars (Strawberry)"), height=2, width=20, bg="#ff5555")[cite: 3]
btn_mars.pack(pady=15)[cite: 3]

btn_neptune = tk.Button(root, text="Neptune (Blueberry)", font=("Arial", 14), 
                        command=lambda: test_select("Neptune (Blueberry)"), height=2, width=20, bg="#55aaff")[cite: 3]
btn_neptune.pack(pady=15)[cite: 3]

# Reset button so you can easily test tapping multiple times
btn_reset = tk.Button(root, text="Reset Screen", font=("Arial", 12), 
                      command=lambda: label.config(text="Space Tea Menu Test\nTap a drink below:", fg="blue"), 
                      height=1, width=15)
btn_reset.pack(pady=30)

# Run the application window loop[cite: 3]
root.mainloop()[cite: 3]