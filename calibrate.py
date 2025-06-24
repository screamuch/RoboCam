import tkinter as tk
from picamera2 import Picamera2
import cv2
from robocam.robocam import RoboCam

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Preview")

        # Picamera2 setup
        self.picam2 = Picamera2()
        self.picam2_config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
        self.picam2.configure(self.picam2_config)
        self.picam2.start()

        # UI Elements
        self.create_widgets()

        self.running = True
        self.robocam = RoboCam(baudrate=115200)

        # Start updating the camera preview
        self.update_preview()

    def create_widgets(self):
        # Camera preview
        self.preview_label = tk.Label(self.root)
        self.preview_label.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # Radio buttons for step size
        self.step_size = tk.DoubleVar(value=1.0)
        tk.Radiobutton(self.root, text="0.1 mm", variable=self.step_size, value=0.1).grid(row=1, column=0)
        tk.Radiobutton(self.root, text="1.0 mm", variable=self.step_size, value=1.0).grid(row=1, column=1)
        tk.Radiobutton(self.root, text="10.0 mm", variable=self.step_size, value=10.0).grid(row=1, column=2)

        # XYZ movement buttons layout
        tk.Button(self.root, text="Y+", command=lambda: self.robocam.move_relative(Y=self.step_size.get())).grid(row=2, column=1)
        tk.Button(self.root, text="X-", command=lambda: self.robocam.move_relative(X=-self.step_size.get())).grid(row=3, column=0)
        tk.Button(self.root, text="X+", command=lambda: self.robocam.move_relative(X=self.step_size.get())).grid(row=3, column=2)
        tk.Button(self.root, text="Y-", command=lambda: self.robocam.move_relative(Y=-self.step_size.get())).grid(row=4, column=1)
        tk.Button(self.root, text="Z-", command=lambda: self.robocam.move_relative(Z=-self.step_size.get())).grid(row=2, column=3)
        tk.Button(self.root, text="Z+", command=lambda: self.robocam.move_relative(Z=self.step_size.get())).grid(row=4, column=3)

        # Position label
        tk.Label(self.root, text="Position:").grid(row=5, column=0, sticky="e")
        self.position_label = tk.Label(self.root, text="0, 0, 0")
        self.position_label.grid(row=5, column=1, columnspan=3, sticky="w")

        # Home buttons
        tk.Button(self.root, text="Home", command=lambda: self.robocam.home()).grid(row=6, column=0, columnspan=2)

    def update_preview(self):
        if self.running:
            # Capture a frame from the camera
            frame = self.picam2.capture_array("main")

            # Convert the frame to RGB and resize for tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))

            # Convert to an image tkinter can use
            photo = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())

            # Update the preview label
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo

            # Format the position using robocam's X, Y, Z values
            position = f"{self.robocam.X}, {self.robocam.Y}, {self.robocam.Z}"
            self.position_label.config(text=position)

            # Schedule the next update
            self.root.after(30, self.update_preview)
            
            # Add crosshair/well outline here to aid with aim

    def on_close(self):
        self.running = False
        self.picam2.stop()
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
