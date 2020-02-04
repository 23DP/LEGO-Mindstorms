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
target = 47 # return value from the reflection senscor when 50% on the line (got by experiment)


''' 
Since this is a general function for staight movement, we have to consider that the robot maz find himself on the
opposite side of the line. drivig_side parameter will tell us wether the robot is facing north or south (from parking's perspective)
If robot is going south, driving_side will equal to -1, since he is on the other side of the line - this is due to imperfect rotation
'''
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
    return sum( lib.diff(steering_history)) #Return the deviation from 0deg 

# main loop
while not any(brick.buttons()):
    os.system('clear') # clearing the terminal for every iteration  

    n = int( input('Parking spot number: ') )  # waiting for a signal that there is a new car
    rotation_side, color = lib.getLogic(n)
    
    offset = drive_straight(1, color) # reach the depth of the parked car

    '''
    offset affects rotation differently depending on the side (clockwise or counter clockwise). If the robot is rotated,
    let's say 2degrees, if he is supposed to rotate 90, he only needs 88degrees (-92 if rotating left)
    NOTE: in reality, this will not be exactly 90degs, due the friction and additional weight (real values found in experiment)
    '''
    rotation_angle = (90 + offset) if n > 3 else (90 - offset)
    robot.drive_time(0, rotation_side*rotation_angle, 1000) #rotate to take a pic
 
    # if theres no input, Yes is default, everything except 'y' will be considered a no
    paid = (input('Confirm payment? [Y/n]') or 'y')
    paid = 1 if paid.lower() == 'y' else 0
    
    if paid:
       brick.sound.file(SoundFile.CHEERING)
    else:
        brick.sound.file(SoundFile.UH_OH)

    robot.drive_time(0, rotation_side*90, 1000) # Rotate to south
    _ = drive_straight(-1, Color.YELLOW)
    robot.drive_time(0, 180, 1000) # Rotate to face the north and rest until the next signal
