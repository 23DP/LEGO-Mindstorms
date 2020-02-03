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
target = 47 # return value from the reflection senscor when 50% on the line


def drive_straight(driving_side: int, color: Color):
    error_history = [] # needed for PID
    steering_history = [] #neded for deviation

    #until he reaches the given spot
    while color_sensor.color() != color : 
        error_history.append( target - color_sensor.reflection() ) #append the error
        steering = lib.PID(error_history, 0.1, 0, 0.1)
        steering_history.append(steering)
        robot.drive(100, driving_side*steering)    

        wait(2) #Wait so we dont change the steering every 0.xx ms


    robot.stop(stop_type = Stop.BRAKE)
    return lib.sum( lib.diff(steering_history)) #Return the deviation from 0deg 


colors_list = [Color.GREEN, Color.RED, Color.BLUE]
def getLogic(n: int):
    rotation = 1 if n < 4 else -1 #rotation direction
    retColor = colors_list[n%3] #this depends on your parking design
    return (rotation, retColor) 
#TODO: move this to lib.py

# main loop
while not any(brick.buttons()):
    os.system('clear') # clearing the terminal for every iteration  

    n = int( input("Parking spot number: ") )# waiting for a signal that there is a new car
    rotation_side, color = getLogic(n)
    
    offset = drive_straight(1, color) # reach the depth of the parked car

    # offset affects rotation differently depending on the side (clockwise or counter clockwise)
    rotation_angle = (90 + offset, 1000) if n > 3 else (90 - offset, 1000)
    robot.drive_time(0, rotation_side*rotation_angle, 1000) #rotate to take a pic
 
    paid = (input('Confirm payment? [Y/n]') or 'y')
    paid = 1 if paid.lower() == 'y' else 0
    
    if paid:
       brick.sound.file(SoundFile.CHEERING)
    else:
        brick.sound.file(SoundFile.UH_OH)

    robot.drive_time(0, rotation_side*90, 1000) # go back to the resting spot
    _ = drive_straight(-1, Color.YELLOW)
    robot.drive_time(0, 180, 1000) # Rotate to face the parking and rest until the next signal
