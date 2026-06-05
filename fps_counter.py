import tkinter as tk
import time
import win32gui
import win32con
import win32api

class FPSOverlay:
    def __init__(self):
        self.root = tk.Tk()
        
        # Configure look and placement
        self.root.title("FPS Counter")
        self.root.geometry("120x40+10+10") # Size (120x40), Positioned at top left (10, 10)
        self.root.overrideredirect(True)   # Removes title bar, borders, and X button
        self.root.config(bg='black')       # Set background to black
        
        # Make it stay always on top
        self.root.attributes("-topmost", True)
        
        # Create text label
        self.label = tk.Label(self.root, text="FPS: --", font=("Consolas", 18, "bold"), fg="#00FF00", bg="black")
        self.label.pack(expand=True)
        
        # Performance variables
        self.last_time = time.time()
        self.frame_count = 0
        
        # Apply native Windows click-through and color-key transparency
        self.root.after(10, self.make_window_transparent)
        
        # Kick off the calculation loop
        self.update_fps()

    def make_window_transparent(self):
        # Fetch the handle of our window
        hwnd = win32gui.FindWindow(None, "FPS Counter")
        
        # Fetch current window styles and add Layered & Transparent behaviors
        extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                               extended_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        
        # Make the color "Black" (0, 0, 0) completely clear/invisible
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)

    def update_fps(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.last_time
        
        # Every 0.5 seconds, refresh the reading
        if elapsed >= 0.5:
            fps = int(self.frame_count / elapsed)
            self.label.config(text=f"FPS: {fps}")
            self.frame_count = 0
            self.last_time = current_time
            
        # Forces a loop cycle as quickly as your system runs
        self.root.after(1, self.update_fps)

if __name__ == "__main__":
    app = FPSOverlay()
    app.root.mainloop()