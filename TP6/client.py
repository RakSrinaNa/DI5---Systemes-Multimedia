import socket
import sys

import cv2
import numpy as np

UDP_PORT = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.10", UDP_PORT))

while True:
    data, addr = sock.recvfrom(320 * 180)
    image = np.frombuffer(data, dtype='int8')
    image = np.uint8(image)
    image = np.reshape(image, (180, 320))
    cv2.imshow("Frame", image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

sock.close()
