import socket
import keyboard
import time
from controlSocket import ControlSocket
import cv2



class PC_Controller:
    def __init__(self):
        self.sock = ControlSocket('192.168.117.1')
        self.sock.run()




    def frame_analysis(self):
        #self.sock.fw()
        #self.sock.bw()
        #self.sock.rotateAngel(1)
        #self.sock.hold()
        #self.sock.exit_All()
        #self.sock.set_speed(200)
        keyboard.on_press_key("w", lambda _:self.sock.fw())
        
        keyboard.on_press_key("h", lambda _:self.sock.hold())
        keyboard.on_press_key("s", lambda _:self.sock.bw())
        keyboard.on_press_key("r", lambda _:self.sock.rotateAngel())
        keyboard.on_press_key("q", lambda _:self.sock.setSpeed(100))
        keyboard.on_press_key("ü", lambda _:self.sock.exit_All())
        while True:
            time.sleep(100)



    def run(self):
        self.frame_analysis()

ctrl = PC_Controller()
ctrl.run()
