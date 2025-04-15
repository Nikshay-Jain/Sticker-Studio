import pyautogui
import time

try:
    print("Move your mouse to the desired location and press Ctrl+C to get the coordinates.")
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='', flush=True)
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print(f"\nCoordinates captured!")
    current_x, current_y = pyautogui.position()
    print(f"X: {current_x}, Y: {current_y}")