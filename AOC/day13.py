from AOC.Solver import Solver
import json
import functools

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.init_part_1()
        self.init_part_2()

    def init_part_1(self):
        self.signals_1 = []
        while True:
            if len(self.first_file_lines) < 2:
                break
            signal = [None, None]
            signal[0] = json.loads(self.first_file_lines.pop(0))
            signal[1] = json.loads(self.first_file_lines.pop(0))
            try:
                self.first_file_lines.pop(0)
            except:
                pass
            self.signals_1.append(signal)

    def init_part_2(self):
        self.signals_2 = []
        for line in self.second_file_lines:
            if len(line.strip()) == 0:
                continue
            signal = json.loads(line)
            self.signals_2.append(signal)
        self.signals_2.append([[2]])            
        self.signals_2.append([[6]])            

    def compare(self, first, second):
        if type(first) != type(second):
            if type(first) == int:
                first = [first]
            else:
                second = [second]
            result = self.compare(first, second)
        elif type(first) == int:
            if first < second:
                result = -1
            elif first > second:
                result = 1
            else:
                result = 0
        else:
            result = 0
            for (i, e_second) in enumerate (second):
                try:
                    e_first = first[i]
                except:
                    if result < 1:
                        result = -1
                    break
                result = self.compare(e_first, e_second)
                if result != 0:
                    break
            if result == 0:
                if len(first) > len(second):
                    result = 1
                else:
                    result = 0

        return(result)

    def first_problem(self):
        result=0
        for (i, signal) in enumerate(self.signals_1):
            if self.compare(signal[0], signal[1]) < 1:
                result += i+1
        return (result)

    def second_problem(self):
        result = 1
        self.signals_2.sort(key = functools.cmp_to_key(self.compare))

        d1 = [[2]]
        d2 = [[6]]

        for (i, l) in enumerate(self.signals_2):
            if self.compare(l,d1) == 0 or self.compare(l, d2) == 0:
                result *= (i+1)

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())