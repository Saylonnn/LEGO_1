#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor,
                                UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from threading import Thread

import time
import sys
sys.path.insert(0, '../PC')
import ball_ev3

ENGINE_LEFT = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
ENGINE_RIGHT = Motor(Port.B, positive_direction=Direction.CLOCKWISE)