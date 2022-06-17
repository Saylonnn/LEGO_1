#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor,
                                UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.iodevices import Ev3devSensor
from threading import Thread
import socket
import threading


class EV3_Controller:
    def __init__(self):
        # EV3 Hardware connect
        self.engine_left = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.engine_right = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
        #self.fS_left = ColorSensor(Port.S1)
        self.gyro = Ev3devSensor(Port.S1)
        #self.fS_right = ColorSensor(Port.S1)
        #self.touch_right = TouchSensor(Port.S3)
        #self.ultrasonic = UltrasonicSensor(Port.S4)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.engine_speed = 200
        self.is_driving_fw = False
        self.is_driving_bw = False

        # Handle Threading
        self.STOP = False

        # Create Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.bind(("", 8484))

    # starts all Methods threaded
    
    #starts server
    def server_control(self):
        

        while True:
            self.sock.listen([1])
            print("now listening on PORT 8484")
            conn, addr = self.sock.accept()
            while True:
                data = conn.recv(1024)
                print("incomming Message: ", data)
                data = data.decode("utf-8")
                if data == "FW":
                    self.fw()
                elif data == "BW":
                    self.bw()
                elif data == "hold":
                    self.hold()
                elif " " in data:
                    x = data.split(" ")
                    if x[0] == "angel":
                        self.rotate(x[1])
                    elif x[0] == "speed":
                        self.set_speed(x[1])
                elif data == "exit":
                    self.exit()
                
                else:
                    self.sock.sendall(bytes("[Execution Error] Data: ", data))
    
    def fw(self):
        self.is_driving_fw = True
        self.is_driving_bw = False
        self.engine_right.run(self.engine_speed)
        self.engine_left.run(self.engine_speed)

    
    def bw(self):
        self.is_driving_bw = True
        self.is_driving_fw = False
        self.engine_right.run(- self.engine_speed)
        self.engine_left.run(- self.engine_speed)
    
    def hold(self):
        self.is_driving_fw = False
        self.is_driving_bw = False
        self.engine_right.hold()
        self.engine_left.hold()
    
    def rotate(self, x):
        self.gyro.reset_angel(0)
        if x > 0:
            self.engine_right.run(self.engine_speed)
            self.engine_left.run(- self.engine_speed)
            if self.gyro.angel() >= x:
                self.hold()
        if x < 0: 
            self.engine_right.run(- self.engine_speed)
            self.engine_left.run(self.engine_speed)
            if self.gyro.angel() <= x:
                self.hold()

    def set_speed(self, speed):
        self.engine_speed = speed
        if self.is_driving_bw == True:
            self.bw()
        if self.is_driving_fw == True:
            self.fw()

    def exit(self):
        self.server_thread.stop()
        exit()


    def run(self):
        server_thread = threading.Thread(target=self.server_control)

        server_thread.start()

        # endless Loop so the programm does not exit
        while self.STOP == False:
            wait(1000)




ev3_control = EV3_Controller()
ev3_control.run()