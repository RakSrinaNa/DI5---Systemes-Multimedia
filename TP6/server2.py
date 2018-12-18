import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np

from videoprocess import videoprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

threads = []
threads.append(videoprocess(10, 1, "192.168.1.10", 5006))
threads.append(videoprocess(10, 2, "192.168.1.10", 5007))
threads.append(videoprocess(10, 3, "192.168.1.10", 5008))

for thread in threads:
    thread.start()

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image.flags.writeable = True
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (320, 180), interpolation=cv2.INTER_LINEAR)
    rawCapture.truncate(0)
    for thread in threads:
        thread.setimage(np.copy(gray))

camera.close()
for thread in threads:
    thread.stop()
