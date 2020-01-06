from functools import  reduce

def sum(arr: list) -> int:
    return reduce(lambda a,b: a+b, arr)

def diff(arr):
    retarr = []
    for i in range(len(arr) - 1):
        retarr.append(arr[i + 1] - arr[i])
    return retarr
