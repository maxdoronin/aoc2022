import datetime
import urllib
from flask import abort

class Solver:
    def __init__(self, request, year, day):
        self.request = request
        self.first_file_lines = None
        self.second_file_lines = None
        if self.request.method == "GET":
            session = self.request.cookies.get("session", None)
            if (session != None):
                url=urllib.request.Request(f"https://adventofcode.com/{year}/day/{day}/input")
                url.add_header ("Cookie", f"session={session}")
                lines = urllib.request.urlopen(url).readlines()
                try:
                    self.first_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)
                except urllib.error.HTTPError as e:     
                    print (e.reason)
                    abort (400)
                lines = urllib.request.urlopen(url).readlines()
                try:
                    self.second_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)
                except urllib.error.HTTPError as e:     
                    print (e.reason)
                    abort (400)
            else:
                abort (400, "GET: Need AOC session cookie to get the input file.\n" +
                "POST: upload 'first' and optionally 'second' input files as multipart/mixed\n")
        elif self.request.method == "POST":
            file = self.request.files.get("first")
            if file != None:
                lines = file.readlines()
                self.first_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)
            else:
                abort (400, "'first' file required")
            file = self.request.files.get("second")
            if file != None:
                lines = file.readlines()
                self.second_file_lines = (l.decode("utf-8").rstrip("\n") for l in lines)
            else:
                self.second_file_lines = None

    def process(self):
        res = ""
        if self.first_file_lines != None:
            res += self.timed_run(self.first_problem)
        else:
            abort (400, "Found no input for the first problem")
        
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

