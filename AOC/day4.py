from AOC.Solver import Solver

class DayXSolver(Solver):
    class Range():
        def __init__(self, r_string):
            (a_string, b_string) = r_string.split("-")
            self.a = int(a_string)
            self.b = int(b_string)
        
        def contains(self, r):
            return (self.a <= r.a <= self.b and self.a <= r.b <= self.b)

        def overlaps_with(self, r):
            return ((self.a <= r.a <= self.b or self.a <= r.b <= self.b) or self.contains(r) or r.contains(self))

    def first_problem(self):
        result=0

        for line in self.first_file_lines:
            (range_1_string, range_2_string) = line.split(",")
            range_1 = self.Range(range_1_string)
            range_2 = self.Range(range_2_string)

            if range_1.contains(range_2) or range_2.contains(range_1):
                result += 1

        return (result)

    def second_problem(self):
        result = 0

        for line in self.second_file_lines:
            (range_1_string, range_2_string) = line.split(",")
            range_1 = self.Range(range_1_string)
            range_2 = self.Range(range_2_string)

            if range_1.overlaps_with(range_2):
                result += 1

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())