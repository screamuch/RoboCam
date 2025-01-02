from .robocam import RoboCam
import time
import RPi.GPIO as GPIO
ON = GPIO.HIGH
OFF = GPIO.LOW

# StentorCam INHERITS from RoboCam class
class StentorCam(RoboCam):
    def __init__(self, baudrate, laser_pin):
        # Printer startup and settings
        self.baud_rate = baudrate
        serial_port = self.find_serial_port()
        if serial_port:
            self.printer_on_serial = self.wait_for_connection(serial_port)

        self.X, self.Y, self.Z = self.update_current_position()
        
        # These settings are specific to the monoprice printer
        self.X_LOWER_LIMIT, self.X_UPPER_LIMIT = 0, 200
        self.Y_LOWER_LIMIT, self.Y_UPPER_LIMIT = 80, 150
        self.Z_LOWER_LIMIT, self.Z_UPPER_LIMIT = 95, 170
        
        # Laser settings
        #self.laser_pin = laser_pin
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.laser_pin, GPIO.OUT)
        
        # Path settings
        self.wells = None
        
        # Camera startup and settings

    # Blue is ground, green is live
    # Purple is ground, orange is live
    def laser_control(self, state=None):
        GPIO.output(self.laser_control, state)
        print(f'[log] laser is {state}')
        
    def move_relative(self, X=None, Y=None, Z=None, speed=None):
        if (X is None or self.X_LOWER_LIMIT <= self.X + X <= self.X_UPPER_LIMIT) and \
           (Y is None or self.Y_LOWER_LIMIT <= self.Y + Y <= self.Y_UPPER_LIMIT) and \
           (Z is None or self.Z_LOWER_LIMIT <= self.Z + Z <= self.Z_UPPER_LIMIT):
            super().move_relative(X, Y, Z, speed)
        else:
            print(f"[error] {self.X, self.Y, self.Z} + {X, Y, Z} is outside of limits, check LOWER_LIMIT and UPPER_LIMIT variables (needs to be thrown as an exception)")
            
    def move_absolute(self, X=None, Y=None, Z=None, speed=None):
        if (X is None or self.X_LOWER_LIMIT <= X <= self.X_UPPER_LIMIT) and \
           (Y is None or self.Y_LOWER_LIMIT <= Y <= self.Y_UPPER_LIMIT) and \
           (Z is None or self.Z_LOWER_LIMIT <= Z <= self.Z_UPPER_LIMIT):
            super().move_absolute(X, Y, Z, speed)
        else:
            print(f"[error] {X, Y, Z} is outside of limits X: {self.X_LOWER_LIMIT <= X <= self.X_UPPER_LIMIT}, Y: {self.Y_LOWER_LIMIT <= Y <= self.Y_UPPER_LIMIT}, Z: {self.Z_LOWER_LIMIT <= Z <= self.Z_UPPER_LIMIT}, check LOWER_LIMIT and UPPER_LIMIT variables (needs to be thrown as an exception)")
        
    # New method to move across the path using absolute locations
    def move_across_path(self, path):
        for loc in path:
            X, Y, Z = loc
            self.move_absolute(X=X, Y=Y, Z=Z)
            self.laser_control(ON)
            time.sleep(3)
            self.laser_control(OFF)
            
    # Blue is ground, green is live
    def laser_control(self, state=None):
        GPIO.output(self.laser_pin, state)
        print(f'[log] laser is {state}')
    
# width = if the well plate is in landscape mode, how many wells are on the long side
# depth = if the well plate is in landscape mode, how many wells are on the short side
# upper_left_loc = [X, Y, Z (optional)] location of left-hand-side farthest from you well
class WellPlatePathGenerator:
    def generate_path(width, depth, upper_left_loc, lower_left_loc, upper_right_loc, lower_right_loc):
        path = []
        
        # Extract coordinates
        x1, y1, z1 = upper_left_loc
        x2, y2, z2 = lower_left_loc
        x3, y3, z3 = upper_right_loc
        x4, y4, z4 = lower_right_loc
        
        # Generate grid of XYZ locations
        for i in range(depth):
            for j in range(width):
                x = x1 + j * (x3 - x1) / (width - 1)
                y = y1 + i * (y2 - y1) / (depth - 1)
                z = z1 + (i * (z2 - z1) / (depth - 1)) + (j * (z3 - z1) / (width - 1))
                
                # Append the location as a 1d tuple
                path.append((x, y, z))
        
        return path
