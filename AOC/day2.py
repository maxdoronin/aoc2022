import datetime
from flask import abort

def process(request):
    res = ""
    if request.method == "GET":
        res = f"""This is {__name__} of AOC2022
It accepts either 'first' file, or 'first' and 'second' files at once as multipart/mixed.
"""
    elif request.method == "POST":
        firstFile = request.files.get("first")
        if firstFile != None:
            res += firstProblem(firstFile)
        else:
            abort (400, "'first' file required")
        
        secondFile = request.files.get("second")
        if secondFile != None:
            res += secondProblem(secondFile)

    return (res)

values = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
scores = [[3, 0, 6],
          [6, 3, 0],
          [0, 6, 3]]

outcomes = {"X": 0, "Y": 3, "Z": 6}

mapping2 = [[3, 1, 2],
          [1, 2, 3],
          [2, 3, 1]]


def firstProblem (f):
    start = datetime.datetime.now()
    
    yourScore = 0

    for line in f.readlines():
        (a, b) = line.strip().split()
        a=a.decode("utf-8")
        b=b.decode("utf-8")

        yourScore += values[b] + 6 - scores[values[a]-1][values[b]-1]

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n{yourScore}")

def secondProblem (f):
    start = datetime.datetime.now()
    
    yourScore = 0

    for line in f.readlines():
        (a, b) = line.strip().split()
        a=a.decode("utf-8")
        b=b.decode("utf-8")

        yourScore += outcomes[b] + mapping2 [values[a]-1][outcomes[b]//3]

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n{yourScore}")
