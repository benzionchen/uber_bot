import pyautogui
import time

# Hardcoded coordinates for the mouse to move to and click
x, y = 1025, 600  # Example coordinates, adjust to your target location

# Move the mouse to the specified coordinates and click
pyautogui.moveTo(x, y, duration=1)  # Move over 1 second
pyautogui.click()  # Perform a left click


# this is for the coordinates of the "Next" button on the "Account Recovery" page
