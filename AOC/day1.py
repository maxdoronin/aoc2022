import datetime
from flask import abort

def process(request):
    res = ""
    if request.method == "GET":
        res = f"""This is {__name__} of AOC2022
It accepts either 'first' file, or 'first' and 'second' files at once.
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
    maxCalories = 0
    currentElfCalories = 0

    for line in f.readlines():
        if len(line.strip()) == 0:
            if currentElfCalories > maxCalories:
                maxCalories = currentElfCalories
            currentElfCalories = 0
        else:
            currentElfCalories += int(line.strip())

    if currentElfCalories > maxCalories:
        maxCalories = currentElfCalories
    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n{maxCalories}\n")

def secondProblem (f):
    start = datetime.datetime.now()
    calories = [0, 0, 0]
    currentElfCalories = 0

    for line in f.readlines():
        if len(line.strip()) == 0:
            minCalories = min(calories)
            if currentElfCalories > minCalories:
                minIndex = calories.index(minCalories)
                calories.pop(minIndex)
                calories.append(currentElfCalories)
            currentElfCalories = 0
        else:
            currentElfCalories += int(line.strip())

    minCalories = min(calories)
    if currentElfCalories > minCalories:
        minIndex = calories.index(minCalories)
        calories.pop(minIndex)
        calories.append(currentElfCalories)
    end = datetime.datetime.now()

    return (f"Second problem: {start} + {end - start}\n{sum(calories)}\n")