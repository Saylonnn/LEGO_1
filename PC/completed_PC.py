import socket
import keyboard
import time
from controlSocket import ControlSocket
import cv2
import threading
import numpy as np
import math
import pickle

class PC_Controller:
    def __init__(self):
        self.IS_CONNECTED = False
        self.EV3_DEV = 1
        self.EvFrontCor = None
        self.EvBackCor = None
        self.BallCor = None
        self.GAME_RUNNING = False
        self.GOAL_1_COR = None
        self.GOAL_2_COR = None
        self.RUNNING = True
    
    
       
    def driveControl(self):
        print("frame_analyse")
       

        while self.GAME_RUNNING == False:
            time.sleep(100)
        
        while GAME_RUNNING == True:
            print("lets start")

            degree = self.calculate_Angle(self.EvFrontCor, self.EvBackCor, self.BallCor)
            self.sock.rotateAngle(degree)
            
            while self.messureDistance(self.evFrontCor, self.BallCor) > 5 and abs(self.calculate_Angle(self.EvFrontCor, self.EvBackCor, self.BallCor)) < 30:  
                self.sock.fw()
            self.sock.hold()
            if self.messureDistance(self.BallCor, self.EvFrontCor) < 5:
                self.sock.grab()
                degree = self.calculateAngle(self.EvFrontCor, self.GOAL_2_COR)
                self.sock.rotateAngle(degree)
                while self.messureDistance(self.EvFrontCor, self.GOAL_2_COR) > 200:
                    self.sock.fw()
                self.sock.shoot()
                self.sock.hold()
        self.driveToStart()
        self.driveControl()

    def driveToStart(self):
        if self.EV3_DEV == 1:
            startPos = (self.GOAL_1_COR[0]+100, self.GOAL_1_COR[1])
            self.sock.hold()
            self.calculateAngle(self.EvFrontCor, startPos)
            self.sock.fw()
            while self.messureDistance(self.EvFrontCor, startPos) > 0:
                time.sleep(10)
            self.sock.hold()
            degree = self.calculateAngle(self.EvFrontCor, (512, 393))
            self.sock.rotateAngle(degree)

        if self.EV3_DEV == 2:
            startPos = (self.GOAL_2_COR[0]-100, self.GOAL_2_COR[1])
            self.sock.hold()
            self.calculateAngle(self.EvFrontCor, startPos)
            self.sock.fw()
            while self.messureDistance(self.EvFrontCor, startPos) > 0:
                time.sleep(10)
            self.sock.hold()
            degree = self.calculateAngle(self.EvFrontCor, (512, 393))
            self.sock.rotateAngle(degree)


 

    def messureDistance(self, ev3Front, ballCor):
        distance = math.sqrt((ev3Front[0] - ballCor[0])**2 + (ev3Front[1] - ballCor[1])**2)
        return distance

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

        #berechne vectoren l??nge
        #l??nge_ev3_vec =  sqrt(a[0]^2 + ... + a[n]^2)
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
        

    def startGame(self):
        self.GAME_STARTED = True
    
    def run_socket(self):
        self.sock = ControlSocket()
        self.sock.run()
        print("control Socket started")
    
    def connectPosManager(self):
        print("connect to position Manager")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.117.132', 8485))
        #connection = self.client_socket.makefile('wb')
        while True:
            data = self.client_socket.recv(2048)
            data = data.decode('utf-8')
            data = data.split(",")
            
            #Ball, EV3_1.Vorne, EV3_1.Hinten, EV3_2.Vorne, EV3_2.Hinten, Tor1_rechts, Tor1_links, Tor2_rechts, Tor2_links
            try:
                self.BallCor = data[0]
                if self.EV3_DEV == 1:
                    self.EvFrontCor = data[1]
                    self.EvBackCor = data[2]
                if self.EV3_DEV == 2:
                    self.EvFrontCor = data[3]
                    self.Ev.BackCor = data[4]
                self.GOAL_1_COR = ((int(data[5][0]) + int(data[6][0]))/2, (int(data[5][1]) + int(data[6][1]))/2)
                self.GOAL_2_COR = ((int(data[7][0]) + int(data[8][0]))/2, (int(data[7][1]) + int(data[8][1]))/2)
                self.CornersCor1 = data[9]
                self.CornersCor2 = data[10]
                self.CornersCor3 = data[11]
                self.CornersCor4 = data[12]
                self.GAME_RUNNING = data[13]
            except:
                print("Error in Position Encoding")
            
            
       
        

        


    def run(self):
            ################################################################
            #           def Threads 
            ################################################################
            ev3_conn = threading.Thread(target=self.run_socket)
            driveController = threading.Thread(target=self.driveControl)
            update_cord = threading.Thread(target=self.connectPosManager)

            ################################################################
            #           start Threads 
            ################################################################
            ev3_conn.start()
            update_cord.start()
            while self.IS_CONNECTED == False:
                time.sleep(100)
            driveController.start()
            
            while self.RUNNING == True:
                time.sleep(100)


ctrl = PC_Controller()
ctrl.run()
