from AOC.Solver import Solver

pp = pprint.PrettyPrinter(indent=4)

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.further_init()
        self.even_further_init()

    def further_init(self):
        self.f = []
        for line in self.first_file_lines:
            num = int(line)
            self.f.append([num, 0])
    
    def even_further_init(self):
        self.f1 = []
        i = 0
        for line in self.first_file_lines:
            num = int(line) * 811589153
            self.f1.append([num, 0, i])
            i += 1

    def process_move(self, f, i):
        f_len = len(f)
        new_pos = i + f[i][0]
        new_pos %= (f_len - 1)
        f[i][1] = 1            
        n = f.pop(i)
        f = f[0:new_pos] + [n] + f[new_pos:]
        return (f)

    def find_nth_item(self, f, n):
        for (k, item) in enumerate (f):
            if item[2] == n:
                return (k)

    def first_problem(self):
        result=0
        f_len = len(self.f)
        i = 0
        while i < len(self.f):
            if self.f[i][1] == 1:
                i += 1
                continue
            else:
                self.f = self.process_move(self.f, i)
        for i in range (f_len):
            if self.f[i][0] == 0:
                break

        result = self.f[(i + 1000) % f_len][0] + self.f[(i + 2000) % f_len][0] + self.f[(i + 3000) % f_len][0]

        return (result)

    def second_problem(self):
        result=0
        f_len = len(self.f1)

        for _ in range (10):
            i = 0
            for i in range (f_len):
                k = self.find_nth_item(self.f1, i)
                self.f1 = self.process_move(self.f1, k)
            for i in range (f_len):
                self.f1[i][1] = 0

        for i in range (f_len):
            if self.f1[i][0] == 0:
                break

        result = self.f1[(i + 1000) % f_len][0] + self.f1[(i + 2000) % f_len][0] + self.f1[(i + 3000) % f_len][0]

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())