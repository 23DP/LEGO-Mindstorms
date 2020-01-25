#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import lib
import LVmodule as LV


right_motor = Motor(Port.C)
left_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S3)
ir_sensor = InfraredSensor(Port.S4)

robot = DriveBase(right_motor, left_motor, 35, 144) 
target = 47

def drive_straight(side: int, color: Color, stops = 1) -> float:
    historic_values = []
    errors = []
    while stops:
        while color_sensor.color() != color : 
            historic_values.append( target - color_sensor.reflection() )
            steering = lib.PID(historic_values, 0.1, 0, 0.1)
            errors.append(steering)
            robot.drive(100, side*steering)    

            wait(2) #Wait so we dont change the steering every 0.xx ms
        stops -= 1
        wait(5)

    robot.stop(stop_type = Stop.BRAKE)
    '''
    TODO: fix the rotation to accurately 90 deg/s, right now 95 is 90 irl
    '''
    return 95 - lib.sum( lib.diff(errors))    

while not any(brick.buttons()):
    
    while:
        takeapic = drive_straight(1, Color.RED, 1)
        robot.drive_time(0, takeapic, 1000) 
        wait(1000)  #Wait 1s to capture the licence plates
        robot.drive_time(0, 95, 1000) 

        rideback = drive_straight(-1, Color.YELLOW)
        robot.drive_time(0, 95, 2000)
    
