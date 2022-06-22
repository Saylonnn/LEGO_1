import socket
import keyboard
import time
from controlSocket import ControlSocket
import cv2
import threading


class PC_Controller:
        
    def frame_analysis(self):
        print("frame_analyse")
        #self.sock.fw()
        #self.sock.bw()
        #self.sock.rotateAngel(1)a
        #self.sock.hold()
        #self.sock.exit_All()
        #self.sock.set_speed(200)
        
        keyboard.on_press_key("w", lambda _:self.sock.fw())
        
        keyboard.on_press_key("h", lambda _:self.sock.hold())
        keyboard.on_press_key("s", lambda _:self.sock.bw())
        keyboard.on_press_key("r", lambda _:self.sock.rotateAngel())
        keyboard.on_press_key("q", lambda _:self.sock.set_speed(100))
        keyboard.on_press_key("ü", lambda _:self.sock.exit_All())
        keyboard.on_press_key("a", lambda _:print("L"))
        while True:
            time.sleep(1)



    def run(self):
        
        keyboard_input = threading.Thread(target=self.frame_analysis)
        server_conn = threading.Thread(target=self.run_socket)
        keyboard_input.start()
        server_conn.start()
    
    def run_socket(self):
        self.sock = ControlSocket('192.168.117.1')
        self.sock.run()


ctrl = PC_Controller()
ctrl.run()
