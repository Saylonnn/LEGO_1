import socket
import keyboard
import time
from controlSocket import ControlSocket
import cv2
import threading
import numpy as np
import math

class PC_Controller:
        
    def frame_analysis(self):
        print("frame_analyse")
        
        
        keyboard.on_press_key("w", lambda _:self.sock.fw())
        
        keyboard.on_press_key("h", lambda _:self.sock.hold())
        keyboard.on_press_key("s", lambda _:self.sock.bw())
        keyboard.on_press_key("r", lambda _:self.sock.rotateAngle(90))
        keyboard.on_press_key("q", lambda _:self.sock.set_speed(1000))
        keyboard.on_press_key("ü", lambda _:self.sock.exit_All())
        keyboard.on_press_key("a", lambda _:print("L"))
        while True:
            time.sleep(1)


    def calculate_Angle(self, ev3_vorne, ev3_hinten, ball_koor):
        ev3_vorne = np.array(ev3_vorne)
        ev3_hinten = np.array(ev3_hinten)
        ball_koor = np.array(ball_koor)
        ev3_mittig = np.array([ev3_vorne[0]-(ev3_vorne[0] - ev3_hinten[0])/2, ev3_vorne[1]-(ev3_vorne[1] - ev3_hinten[1])/2])
        print("EV3 Mittig: ", ev3_mittig)
        ev3_vec = ev3_vorne - ev3_mittig
        ball_vec = ball_koor - ev3_mittig
        print("ev3_vec: ", ev3_vec)
        print("ball_vec: ", ball_vec)

        #calculate_Angle
        #Skalarprodukt --> a_1 * b_1 +.... a_n + b_n
        skalar_produkt = ev3_vec.dot(ball_vec)
        print("skalar_prod: ", skalar_produkt)

        #berechne vectoren länge
        #länge_ev3_vec =  sqrt(a[0]^2 + ... + a[n]^2)
        x = 0
        for i in range(0, ev3_vec.size):
            x = x + ev3_vec[i]**2
        length_ev3_vec = math.sqrt(x)
        print("length_ev3_vec: ", length_ev3_vec)
       
        x = 0
        for i in range(0, ball_vec.size):
            x = x + ball_vec[i]**2
        length_ball_vec = math.sqrt(x)
        print("length_ball_vec: ", length_ball_vec)

        degree = math.degrees(math.acos(skalar_produkt / (length_ball_vec * length_ev3_vec)))
        print("degree: ", degree)
        return degree
        

    def run(self):
        self.calculate_Angle([3,3], [3,1], [1,2])
        #keyboard_input = threading.Thread(target=self.frame_analysis)
        #server_conn = threading.Thread(target=self.run_socket)
        #keyboard_input.start()
        #server_conn.start()
    
    def run_socket(self):
        self.sock = ControlSocket('192.168.117.1')
        self.sock.run()


ctrl = PC_Controller()
ctrl.run()
