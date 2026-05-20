import pyautogui
import keyboard
import time

# Set the trigger key
START_KEY = 'f6'

print(f"Waiting for you to press {START_KEY}...")

# This waits for the key to be pressed globally
keyboard.wait(START_KEY)

print("Key detected! Starting clicks...")

# Optional: tiny delay so the key release doesn't interfere
time.sleep(0.5)

try:
    while True:
        pyautogui.click()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")
