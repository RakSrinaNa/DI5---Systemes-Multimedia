import socket
import time
from threading import Thread

import cv2


class videoprocess(Thread):
    def __init__(self, fps: int, id: int, ipclient: str, portclient: int):
        Thread.__init__(self)
        self.image = None
        self.fps = fps
        self.id = id
        self.ipclient = ipclient
        self.portclient = portclient
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stop = False
        self.currfps = 0
        self.lastTime = time.time()
        print('thread=live at fps=' + str(fps))

    def stop(self):
        self.stop = True

    def setimage(self, image):
        self.image = image
        cv2.putText(self.image, "fps={fps}".format(fps=self.currfps), (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    def run(self):
        print('run thread={id}'.format(id=self.id))
        while not self.stop:
            self.currfps = 1.0 / (time.time() - self.lastTime)
            self.lastTime = time.time()
            if self.image is not None:
                self.sock.sendto(self.image, (self.ipclient, self.portclient))
            attente = 1 / float(self.fps)
            time.sleep(attente)
