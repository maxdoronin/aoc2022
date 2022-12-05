import datetime
from flask import abort

class Solver:
    def __init__(self, request):
        self.request = request
        self.first_file_lines = None
        self.second_file_lines = None
        if self.request.method == "POST":
            file = self.request.files.get("first")
            if file != None:
                lines = file.readlines()
                self.first_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)
            file = self.request.files.get("second")
            if file != None:
                lines = file.readlines()
                self.second_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)

    def process(self):
        res = ""
        if self.request.method == "GET":
            res = f"""This is {__name__} of AOC
It accepts either 'first' file, or 'first' and 'second' files at once as multipart/mixed.
"""
        elif self.request.method == "POST":
            if self.first_file_lines != None:
                res += self.timed_run(self.first_problem)
            else:
                abort (400, "'first' file required")
            
            if self.second_file_lines != None:
                res += self.timed_run(self.second_problem)

        return (res)
    
    def timed_run(self, f: callable):
        start = datetime.datetime.now()
        result = f()
        end = datetime.datetime.now()
        return (f"{f.__qualname__}: {start} + {end - start}\n{result}\n")

    def first_problem(self):
        return ("first_problem is not implemented")

    def second_problem(self):
        return ("second_problem is not implemented")

