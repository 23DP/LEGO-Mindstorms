#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from lib import sum, diff


right_motor = Motor(Port.C)
left_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S3)
ir_sensor = InfraredSensor(Port.S4)

robot = DriveBase(right_motor, left_motor, 35, 144) 

def drive_straight(side: int, target: int, color: Color) ->int:
    steering = []
    while color_sensor.color() != color : 
        error = target - color_sensor.reflection()
        robot.drive(100, side*error/9)   
        steering.append(error/9)    

        wait(2) #Wait so we dont change the steering every 0.xx ms
    robot.stop(stop_type = Stop.BRAKE)
    '''
    TODO: fix the rotation to accurately 90 deg/s, right now 95 is 90 irl
    '''
    return 95 - sum(diff(steering))    

while not any(brick.buttons()):
'''
TODO: move more than just to the first line
'''
    takeapic = drive_straight(1, 47, Color.RED)
    robot.drive_time(0, takeapic, 1000) 
    wait(1000)  #Wait 1s to capture the licence plates
    robot.drive_time(0, 95, 1000) 

    rideback = drive_straight(-1, 47, Color.YELLOW)
    robot.drive_time(0, 95, 2000)

