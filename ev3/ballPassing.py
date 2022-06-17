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

enginePass = Motor(Port.C, positive_direction=Direction.CLOCKWISE)

# Code here

