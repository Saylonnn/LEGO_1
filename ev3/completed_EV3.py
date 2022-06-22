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
import sys


class EV3_Controller:
    def __init__(self):
        # EV3 Hardware connect
        self.engine_left = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
        self.engine_right = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
        #self.fS_left = ColorSensor(Port.S1)
        self.gyro = Ev3devSensor(Port.S1)
        #self.gyro.mode("GYRO")
        #self.gyro.calibrate()
        print(self.gyro.read("ANALOG-0"))
        #self.fS_right = ColorSensor(Port.S1)
        #self.touch_right = TouchSensor(Port.S3)
        #self.ultrasonic = UltrasonicSensor(Port.S4)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.engine_speed = 200
        self.is_driving_fw = False
        self.is_driving_bw = False

        # Handle Threading
        self.STOP = False
        self.server_thread = threading.Thread(target=self.server_control)

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
            print("connected by: ", addr)
            while True:
                data = conn.recv(1024)
                print("incomming Message: ", data)
                data = data.decode("utf-8")
                print(data)
                if data == "FW":
                    self.fw()
                elif data == "BW":
                    self.bw()
                elif data == "hold":
                    self.hold()
                elif " " in data:
                    x = data.split(" ")
                    if x[0] == "angle":
                        self.rotate(int(x[1]))
                    elif x[0] == "speed":
                        self.set_speed(int(x[1]))
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
        
        #self.gyro.reset(0)
        current_angle = self.gyro.read("ANALOG-0")[0]
        print("current_angle: ", current_angle)
        new_angle = int(current_angle) + int(x)
        print("new_angle: ", new_angle)
        if new_angle > current_angle:
            
            self.engine_right.run(-self.engine_speed)
            self.engine_left.run( self.engine_speed)
            while self.gyro.read("ANALOG-0")[0] <= new_angle:
                print(self.gyro.read("ANALOG-0")[0])
            self.hold()
            print("angel finished")
                    
                
        if new_angle < current_angle: 
            self.engine_right.run( self.engine_speed)
            self.engine_left.run(- self.engine_speed)
            while self.gyro.read("ANALOG-0")[0] >= new_angle:
                print(self.gyro.read("ANALOG-0")[0])
            self.hold()
            print("angel finished")
                    
                

    def set_speed(self, speed):
        self.engine_speed = speed
        if self.is_driving_bw == True:
            self.bw()
        if self.is_driving_fw == True:
            self.fw()

    def exit(self):
        #self.server_thread.exit()
        sys.exit()


    def run(self):
        

        self.server_thread.start()

        # endless Loop so the programm does not exit
        while self.STOP == False:
            wait(1000)




ev3_control = EV3_Controller()
ev3_control.run()



'''

class MySensor(Ev3devSensor):
    """Example of extending the Ev3devSensor class."""
    def __init__(self, port):
        """Initialize the sensor."""
        # Initialize the parent class.
        super().__init__(port)
        # Get the sysfs path.
        self.path = '/sys/class/lego-sensor/sensor' + str(self.sensor_index)
    def get_modes(self):
        """Get a list of mode strings so we don't have to look them up."""
        # The path of the modes file.
        modes_path = self.path + '/modes'
        # Open the modes file.
        with open(modes_path, 'r') as m:

            # Read the contents.
            contents = m.read()
            # Strip the newline symbol, and split at every space symbol.
            return contents.strip().split(' ')
# Initialize the sensor
sensor = MySensor(Port.S1)
# Show where this sensor can be found
print(sensor.path)
# Print the available modes
modes = sensor.get_modes()
print(modes)
# Read mode 0 of this sensor
while True:
    gyroValueRaw = open(sensor._path + "/value0", "rb")
    print(gyroValueRaw)
'''