from robocam.stentorcam import StentorCam, WellPlatePathGenerator
from robocam.pihqcamera import PiHQCamera
from robocam.robocam import RoboCam
import time

robocam = RoboCam(baudrate=115200)
camera = PiHQCamera(resolution=(1280, 1024))

robocam.home()

path = WellPlatePathGenerator.generate_path(width=8, depth=6, upper_left_loc=(50.3, 145.4, 144.1), lower_left_loc=(50.3, 81.3, 144.1), upper_right_loc=(141.8, 146.6, 144.1), lower_right_loc=(141.5, 81.8, 144.1))

for index, loc in enumerate(path):
	X, Y, Z = loc
	robocam.move_absolute(X=X, Y=Y, Z=Z)
	time.sleep(1) # to compensate for shakes
    
	photo_path = f"index-{index}_loc-{loc}_timestamp-{time.strftime('%Y%m%d_%H%M%S')}.png"
	camera.take_photo_and_save(photo_path)
    
	time.sleep(2)
    
