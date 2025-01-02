import RPi.GPIO as GPIO

class Laser:
    ON = GPIO.HIGH
    OFF = GPIO.LOW

    def __init__(self, laser_pin):
        # Laser settings
        self.laser_pin = laser_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser_pin, GPIO.OUT)
        GPIO.output(self.laser_pin, self.OFF)
        
    # Blue is ground, green is live
    def switch(self, state=None):
        GPIO.output(self.laser_pin, state)
        print(f'[log] laser is {state}')
