#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import lib, os


#defining all sensors and motors that will be used
right_motor = Motor(Port.C)
left_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S3)

robot = DriveBase(right_motor, left_motor, 35, 144) #Initialization of a driving base
target = 47


def drive_straight(driving_side: int, color: Color):
    error_history = [] # needed for PID
    steering_history = [] #neded for deviation

    while color_sensor.color() != color : 
        error_history.append( target - color_sensor.reflection() )
        steering = lib.PID(error_history, 0.1, 0, 0.1)
        steering_history.append(steering)
        robot.drive(100, driving_side*steering)    

        wait(2) #Wait so we dont change the steering every 0.xx ms


    robot.stop(stop_type = Stop.BRAKE)
    return lib.sum( lib.diff(steering_history))    


color = [Color.GREEN, Color.RED, Color.BLUE]
def getLogic(n: int):
    rotation = 1 if n < 4 else -1 #rotation direction
    retColor = color[n%3]
    return (rotation, retColor) 


# main loop
while not any(brick.buttons()):
    os.system('clear')    

    n = int( input("Broj parking mesta: ") )# waiting for a signal that there is a new car
    rotation_side, color = getLogic(n)

    offset = drive_straight(1, color)
    rotation_angle = (90 + offset, 1000) if n > 3 else (90 - offset, 1000)
    wait(20)
    robot.drive_time(0, rotation_side*rotation_angle, 1000) #rotate
 
    paid = (input('Da li je placeno? [Y/n]') or 'y')
    paid = 1 if paid.lower() == 'y' else 0
    
    if paid:
       brick.sound.file(SoundFile.CHEERING)
    else:
        brick.sound.file(SoundFile.UH_OH)

    robot.drive_time(0, rotation_side*90, 1000) 

    _ = drive_straight(-1, Color.YELLOW)
    robot.drive_time(0, 90, 2000) #90 degrees for 2 seconds = 180
