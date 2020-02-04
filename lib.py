from pybricks import Color
'''
NOTE: yes, diff already exists in numpy, but the robot has no internet access, so we had to make our own
'''

#returns the difference between adjacent list elements
def diff(arr):
    retarr = []
    for i in range(len(arr) - 1):
        retarr.append(arr[i + 1] - arr[i])
    return retarr


colors_list = [Color.GREEN, Color.RED, Color.BLUE]
def getLogic(n: int):
    rotation = 1 if n < 4 else -1 #rotation direction
    retColor = colors_list[n%3]   #this depends on your parking design
    return (rotation, retColor) 


#improvised PID, since we don't have the model of our system
def PID(values: list, kp: float, ki: float, kd: float) -> float:
    integral = sum(values[-4:])         # sum of last 4 errors, so that not all errors affect the steering
    derivative = sum(diff(values[-2:])) # how fast does the error change
    return kp*values[-1] + ki*integral + kd*derivative  #PID formula
