import sys
from typing import Optional, Tuple
from PIL import Image
import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import ttk

def select_region_and_capture(coords: dict, save_screenshot: bool = True) -> tuple[tuple[int, int, int, int], Image.Image]:
    """Display a window to select the region, and capture the selected region."""

    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Create a window to select the region in fullscreen mode
    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        "Select Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("Select Region", draw_rectangle, param=coords)

    while True:
        img_copy = img.copy()
        if coords["drawing"]:
            cv2.rectangle(
                img_copy,
                (coords["ix"], coords["iy"]),
                (coords["x_end"], coords["y_end"]),
                (0, 255, 0),
                2,
            )
        elif coords["ix"] != -1 and coords["iy"] != -1:
            cv2.rectangle(
                img_copy,
                (coords["ix"], coords["iy"]),
                (coords["x_end"], coords["y_end"]),
                (0, 255, 0),
                2,
            )

        # Create a mask around the selected region
        mask = np.zeros(img_copy.shape, dtype=np.uint8)
        roi_corners = np.array([[(coords["ix"], coords["iy"]), (coords["x_end"], coords["iy"]), (coords["x_end"], coords["y_end"]), (coords["ix"], coords["y_end"])]], dtype=np.int32)
        channel_count = img_copy.shape[2]
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)

        # Create an inverse mask of the selected region
        inverse_mask = cv2.bitwise_not(mask)

        # Apply the mask (set the mask's opacity)
        opacity = -0.1
        img_copy = cv2.addWeighted(inverse_mask, opacity, img_copy, 1, 0)

        cv2.imshow("Select Region", img_copy)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # Press 'Esc' to exit the program
            cv2.destroyAllWindows()
            sys.exit(0)
        elif key == 13 or coords["selected_region"]:  # Press 'Enter' to confirm the selection
            if (
                coords["ix"] != -1
                and coords["iy"] != -1
                and coords["x_end"] != -1
                and coords["y_end"] != -1
            ):
                break

    cv2.destroyAllWindows()
    region = get_region_coordinates(coords)
    #print(region)

    # Use pyautogui.screenshot to capture the region based on the given coordinates
    screenshot_region = pyautogui.screenshot(region=region)

    # Convert the region screenshot to a PIL Image object
    screenshot_region = Image.frombytes(
        "RGB",
        (screenshot_region.width, screenshot_region.height),
        screenshot_region.tobytes(),
    )
    
    if save_screenshot:
        screenshot_region.save("screenshot.png")

    return (region, screenshot_region)

def draw_rectangle(event, x, y, flags, param) -> None:
    """Draw a rectangle on the image when the mouse is clicked and dragged"""
    coords = param  # Get the coordinates dictionary from the 'param' argument

    if event == cv2.EVENT_LBUTTONDOWN:
        if not coords["drawing"]:
            coords["drawing"] = True
            coords["ix"], coords["iy"] = x, y
            # Set initial coords when first clicked
            coords["x_end"], coords["y_end"] = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if coords["drawing"]:
            coords["x_end"], coords["y_end"] = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        coords["drawing"] = False
        coords["x_end"], coords["y_end"] = x, y
        coords["selected_region"] = True

def get_region_coordinates(coords: dict) -> Tuple[int, int, int, int]:
    """Get the coordinates of the region of interest (ROI)"""
    # Ensure that the coordinates are ordered correctly
    x_start, x_end = min(coords["ix"], coords["x_end"]), max(
        coords["ix"], coords["x_end"]
    )
    y_start, y_end = min(coords["iy"], coords["y_end"]), max(
        coords["iy"], coords["y_end"]
    )

    return x_start, y_start, x_end - x_start, y_end - y_start

def create_window_always_on_top():
    global clicked
    clicked = False # When clicked on the button

    win = tk.Tk()
    win.geometry("250x100")
    win.title("Screen Cropper")

    def on_click():
        global clicked
        clicked = True
        #print(win.winfo_x(), win.winfo_y())
        # Make window invisible/destroy and fast, before taking a screenshot
        win.attributes('-alpha',0.0) # doesn't show animation like destroy() or withdraw()
        win.destroy()

    def check_exit():
        # For checking CTRL+^C or other signals
        win.after(250, check_exit)

    # Create button
    frame = ttk.Frame(win)
    style = ttk.Style()
    style.configure('TButton', 
                    font =('calibri', 11, 'bold'),
                    borderwidth = '4')
    ttk.Button(frame, text="Crop screen", style="TButton", command=on_click).pack()

    frame.pack(expand=True)

    # Make window always on top
    win.attributes('-topmost',True)

    # Called every 250ms to check signals
    win.after(250, check_exit)

    # Blocks until window is destroyed
    win.mainloop()
    
    # After main loop
    if clicked:
        coords = {"ix": -1, "iy": -1, "x_end": -1, "y_end": -1, "drawing": False, "selected_region": False}
        select_region_and_capture(coords)

def run():
    create_window_always_on_top()

def crop(save_screenshot: bool = True) -> Tuple[Tuple[int, int, int, int], Image.Image]:
    coords = {"ix": -1, "iy": -1, "x_end": -1, "y_end": -1, "drawing": False, "selected_region": False}
    return select_region_and_capture(coords, save_screenshot)

if __name__ == "__main__":
    run()
