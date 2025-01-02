from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time

class PiHQCamera():
    def __init__(self, resolution=(1920, 1080), exposure=0, gain=0, red_gain=0, blue_gain=0):
        self.preset_resolution = resolution
        self.picam2 = Picamera2()
        self.config = self.picam2.create_still_configuration(main={"size": resolution})
        self.picam2.configure(self.config)
        #self.picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain}) #, "RedGain": red_gain, "BlueGain": blue_gain}) # those aren't working right now
        
    def start(self):
        self.picam2.start()

    def set_resolution(self, width, height):
        self.config = self.picam2.create_still_configuration(main={"size": (width, height)})
        self.picam2.configure(self.config)

    def set_exposure(self, exposure):
        self.picam2.set_controls({"ExposureTime": exposure})

    def set_gain(self, gain):
        self.picam2.set_controls({"AnalogueGain": gain})

    # def set_color_gains(self, red_gain=None, blue_gain=None):
    #     self.picam2.set_controls({"RedGain": red_gain, "BlueGain": blue_gain})
    
    def set_color_gains(self, red_gain=1.0, blue_gain=1.0):
        self.picam2.set_controls({"ColourGains": (red_gain, blue_gain)})

    def take_photo_and_save(self, file_path=None):
        self.picam2.stop()
        self.config = self.picam2.create_still_configuration(main={"size": resolution})
        self.picam2.configure(self.config)
        if file_path is None:
            file_path = f"{time.strftime('%Y%m%d_%H%M%S')}.png"
        self.picam2.switch_mode_and_capture_file(self.config, file_path)

    def start_recording_video(self, video_path=None):
        self.picam2.stop()
        config = self.picam2.create_video_configuration(main={"size": self.preset_resolution})
        self.picam2.configure(config)
        if video_path is None:
            video_path = f"{time.strftime('%Y%m%d_%H%M%S')}.h264"
        encoder = H264Encoder()
        output = FileOutput(video_path)
        self.picam2.start_recording(encoder, output)

    def stop_recording_video(self):
        self.picam2.stop_recording()
