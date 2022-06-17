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
        keyboard.on_press_key("w", lambda _:s.sendall(b'FW'))
        
        keyboard.on_press_key("s", lambda _:s.sendall(b"BW"))
        keyboard.on_press_key("s", lambda _:s.sendall(b"hold"))
        keyboard.on_press_key("r", lambda _:s.sendall(b"angel 50"))
        keyboard.on_press_key("q", lambda _:s.sendall(b"speed 100"))
        keyboard.on_press_key("ü", lambda _:s.sendall(b"exit"))




    def run(self):
        self.frame_analysis()
