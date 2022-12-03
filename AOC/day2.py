from AOC.Solver import Solver

class DayXSolver(Solver):
    values = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}

    scores = [[3, 0, 6],
            [6, 3, 0],
            [0, 6, 3]]

    outcomes = {"X": 0, "Y": 3, "Z": 6}

    mapping2 = [[3, 1, 2],
            [1, 2, 3],
            [2, 3, 1]]

    def first_problem(self):
        result=0

        for line in self.first_file_lines:
            (a, b) = line.split()

            result += self.values[b] + 6 - self.scores[self.values[a]-1][self.values[b]-1]

        return (result)

    def second_problem(self):
        result = 0

        for line in self.second_file_lines:
            (a, b) = line.split()
            result += self.outcomes[b] + self.mapping2 [self.values[a]-1][self.outcomes[b]//3]
        
        return (result)

def process(request):
    solver = DayXSolver(request)
    return (solver.process())
