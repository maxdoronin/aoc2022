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
            res += first_problem(firstFile)
        else:
            abort (400, "'first' file required")
        
        secondFile = request.files.get("second")
        if secondFile != None:
            res += second_problem(secondFile)

    return (res)

def letter_value(letter):
    if letter.isupper():
        return (ord(letter) - ord("A") + 1 + 26)
    else:
        return (ord(letter) - ord("a") + 1) 

def first_problem (f):
    start = datetime.datetime.now()

    result = 0

    for rucksack in f.readlines():
        rucksack = rucksack.strip().decode("utf-8")
        compartment_1 = rucksack[:len(rucksack)//2]
        compartment_2 = rucksack[len(rucksack)//2:]

        checked_items = set()
        overlapping_items = set()

        for item in compartment_1:
            if item not in checked_items:
                checked_items.add(item)
                if (item not in overlapping_items) and (item in compartment_2):
                    overlapping_items.add(item)
        
        for item in overlapping_items:
            result += letter_value(item)

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n{result}\n")

def second_problem (f):
    start = datetime.datetime.now()

    result = 0

    lines = iter(f.readlines())
    badges = list()
    while (rucksack_1 := next(lines, None)) is not None:
        # assume the number of rucksacks is always 3n
        # convert to set for O(1) search
        rucksack_1 = set(rucksack_1.strip().decode("utf-8"))
        rucksack_2 = set(next(lines).strip().decode('utf-8'))
        rucksack_3 = set(next(lines).strip().decode('utf-8'))

        for item in rucksack_1:
            if item in rucksack_2 and item in rucksack_3:
                badges.append(item)
                break

    for item in badges:
        result += letter_value(item)

    end = datetime.datetime.now()

    return (f"First problem: {start} + {end - start}\n{result}\n")