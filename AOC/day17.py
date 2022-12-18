from AOC.Solver import Solver
import numpy as np

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)

    def further_init(self):
        self.jet_values = {"<": -1, ">": 1}
        self.jets = self.first_file_lines[0]
        self.current_jet = 0
        self.jet_sequence_len = len(self.jets)
        self.tunnel_width = 7
        self.tunnel_depth = 8
        self.initial_rock_row = self.tunnel_depth - 4
        self.top_of_rock_stack = self.tunnel_depth - 1
        self.initial_rock_col = 2
        self.top_of_stack = 0
        self.tunnel = np.full((self.tunnel_depth, self.tunnel_width), 0, dtype=np.ubyte)

    def rocks_init(self):
        rock_1 = np.array([[1,1,1,1]], dtype=np.ubyte)
        rock_2 = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=np.ubyte)
        rock_3 = np.array([[0,0,1],[0,0,1],[1,1,1]], dtype=np.ubyte)
        rock_4 = np.array([[1],[1],[1],[1]], dtype=np.ubyte)
        rock_5 = np.array([[1,1],[1,1]], dtype=np.ubyte)
        self.rocks = [rock_1, rock_2, rock_3, rock_4, rock_5]
        self.current_rock = 0
        self.rock_sequence_len = len(self.rocks)

    def get_jet(self):
        result = self.jet_values[self.jets[self.current_jet % self.jet_sequence_len]]
        self.current_jet += 1
        return (result)

    def get_rock(self):
        result = self.rocks[self.current_rock % self.rock_sequence_len]
        self.current_rock += 1
        return (result)

    def try_lateral(self, rock, row, col, jet):
        rock_height = rock.shape[0]
        rock_width = rock.shape[1]
        if (col + jet < 0) or (col + rock_width + jet > self.tunnel_width):
            return (row, col, False)
        else:
            tunnel_segment = self.tunnel[row - rock_height + 1:row + 1, col + jet:col + jet + rock_width]
            overlap = np.add(tunnel_segment, rock)
            if 2 in overlap:
                return (row, col, False)
            else:
                col += jet
                return (row, col, True)

    def try_vertical(self, rock, row, col):
        rock_height = rock.shape[0]
        rock_width = rock.shape[1]
        if row + 1 == self.tunnel_depth:
            return (row, col, False)
        else:
            tunnel_segment = self.tunnel[row - rock_height + 2:row + 2,col:col + rock_width]
            overlap = np.add(tunnel_segment, rock)
            if 2 in overlap:
                return (row , col, False)
            else:
                row += 1
                return (row, col, True)

    def rock_fall(self, rock, row, col):
        rock_height = rock.shape[0]
        rock_width = rock.shape[1]
        falling = True
        while falling:
            jet = self.get_jet()
            (row, col, _) = self.try_lateral(rock, row, col, jet)
            (row, col, falling) = self.try_vertical(rock, row, col)
        else:
            self.tunnel[row - rock_height + 1:row + 1, col:col+rock_width] = np.add(self.tunnel[row - rock_height + 1:row + 1, col:col+rock_width], rock)
        
    def set_top_of_rock_stack(self):
        while sum(self.tunnel[self.top_of_rock_stack]) > 0:
            last_line = self.tunnel[self.top_of_rock_stack]
            self.tunnel = np.vstack([[0]*7, self.tunnel])
            self.tunnel_depth += 1
        if (self.tunnel.shape[0] > 100):
            self.tunnel = self.tunnel[:-10, :]

    def first_problem(self):
        result=0
        self.further_init()
        self.rocks_init()
        for _ in range (2022):
            rock = self.get_rock()
            row = self.initial_rock_row
            col = self.initial_rock_col
            self.rock_fall(rock, row, col)
            self.set_top_of_rock_stack()
        result = self.tunnel_depth - 8
        return (result)

    def second_problem(self):
        result=0
        rock_count = 1000000000000
        unperiodic_rock_sequence_end = 1741
        rock_period = 1725
        depth_period = 2659
        self.further_init()
        self.rocks_init()
        for _ in range (unperiodic_rock_sequence_end):
            rock = self.get_rock()
            row = self.initial_rock_row
            col = self.initial_rock_col
            self.rock_fall(rock, row, col)
            self.set_top_of_rock_stack()

        periods = (rock_count - unperiodic_rock_sequence_end) // rock_period
        remaining_rocks = (rock_count - unperiodic_rock_sequence_end) % rock_period
        self.tunnel_depth += periods*depth_period

        for i in range (remaining_rocks):
            rock = self.get_rock()
            row = self.initial_rock_row
            col = self.initial_rock_col
            self.rock_fall(rock, row, col)
            self.set_top_of_rock_stack()

        result = self.tunnel_depth - 8
        return (result)
def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())