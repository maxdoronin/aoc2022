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

def firstProblem (f):
    start = datetime.datetime.now()

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n")

def secondProblem (f):
    start = datetime.datetime.now()

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n")
