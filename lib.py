# returns the sum of all elements in passed list
def sum(arr: list):
    sum = 0
    for element in arr:
        sum += element
    return sum

#returns the difference between adjacent list elements
def diff(arr):
    retarr = []
    for i in range(len(arr) - 1):
        retarr.append(arr[i + 1] - arr[i])
    return retarr

#improvised PID, since we don't have the model of our system
def PID(values: list, kp: float, ki: float, kd: float) -> float:
    integral = sum(values[-4:])         # sum of last 4 errors
    derivative = sum(diff(values[-2:])) # how fast does the error change
    return kp*values[-1] + ki*integral + kd*derivative  #PID formula
