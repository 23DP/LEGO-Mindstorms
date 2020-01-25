def sum(arr: list) -> float:
    sum = 0
    for element in arr:
        sum += element
    return sum

def diff(arr):
    retarr = []
    for i in range(len(arr) - 1):
        retarr.append(arr[i + 1] - arr[i])
    return retarr

def PID(values: list, kp: float, ki: float, kd: float) -> float:
    integral = sum(values[-4:])
    derivative = sum(diff(values[-4:]))
    return kp*values[-1] + ki*integral + kd*derivative
