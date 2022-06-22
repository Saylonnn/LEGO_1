#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor,
                                 UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from threading import Thread
import socket

# Own imports
import time
import sys

# Initializing EV3 Brick and required parts

ev3 = EV3Brick()

ENGINE_LEFT = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
ENGINE_RIGHT = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
ENGINE_PASS_L = Motor(Port.C, positive_direction=Direction.CLOCKWISE)   # Left engine for cathcing and shooting the ball
ENGINE_PASS_R = Motor(Port.D, positive_direction=Direction.CLOCKWISE)   # Right engine for catching and shooting the ball

# Code here
class BallPassing:

    # Shooting engines move swiftly opening the cage and pushing the ball out
    def shoot():
        ENGINE_PASS_L.run(1000)
        ENGINE_PASS_R.run(1000)
        time.sleep(0.2)
        ENGINE_PASS_L.stop()
        ENGINE_PASS_R.stop()

    # Robot moves forward and closes the cage
    def close_cage():
        ENGINE_LEFT.run(500)
        ENGINE_RIGHT.run(500)
        ENGINE_PASS_L.run(-100)
        ENGINE_PASS_R.run(-100)
        time.sleep(0.9)
        ENGINE_LEFT.stop()
        ENGINE_RIGHT.stop()
        ENGINE_PASS_L.stop()
        ENGINE_PASS_R.stop()


#bp = BallPassing
#bp.close_cage()
#bp.shoot()
