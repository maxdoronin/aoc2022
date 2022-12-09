from AOC.Solver import Solver
import numpy as np

class DayXSolver(Solver):
    class Rope():
        class Board():
            def __init__(self, board_v_size, board_h_size):
                # self.board_size = board_size
                self.board = np.chararray((board_v_size, board_h_size), unicode=True, itemsize=1)
                self.board[:] = "."
            
            def get_board_value(self, r, c):
                return (self.board[r][c])

            def set_board_value(self, r: int, c: int, v: str):
                self.board[r][c]=v
            
            def __str__(self):
                return self.board.__str__()
            
            def __repr__(self):
                return self.board.__str__()

        class RC():
            def __init__(self, r, c):
                self.r = r
                self.c = c
                self.command_map = {"U": self.move_up, "D": self.move_down, "L": self.move_left, "R": self.move_right}
            
            def set_pos(self, r, c):
                self.r = r
                self.c = c
            
            def get_pos(self):
                return (self.r, self.c)

            def move_left(self, p=1):
                self.c -= p
            
            def move_right(self, p=1):
                self.c += p
            
            def move_up(self, p=1):
                self.r -= p

            def move_down(self, p=1):
                self.r += p

            def move(self, command_code, parameter):
                command = self.command_map[command_code]
                command(parameter)
            
            def follow(self, rc):
                rd = self.r_delta(rc)
                cd = self.c_delta(rc)
                if (abs(rd) == 2 or abs(cd) == 2):
                    if (abs(rd) > 0):
                        self.r += rd//abs(rd)
                    if (abs(cd) > 0):
                        self.c += cd//abs(cd)

            def r_delta(self, rc):
                return (rc.r - self.r)
            
            def c_delta(self, rc):
                return (rc.c - self.c)
            
            def __str__(self):
                return (f"r:{self.r}, c:{self.c}")

            def __repr__(self):
                return self.__str__()

        def __init__(self, board_v_size, board_h_size, knots):
            self.board = self.Board(board_v_size, board_h_size)
            self.knots = list()
            for i in range(knots):
                self.knots.append(self.RC(board_v_size // 2 , board_h_size // 2))
        
        def move(self, command_code, parameter):
                for i in range(parameter):
                    self.knots[0].move(command_code, 1)
                    for knot_index in range(1, len(self.knots)):
                        self.knots[knot_index].follow(self.knots[knot_index - 1])

                    (r, c) = self.knots[-1].get_pos()
                    self.board.set_board_value(r, c, "#")

        def __str__(self):
            res = ""
            for knot in self.knots:
                res += f"({knot.r}, {knot.c})"
            return (res)
        
        def __repr__(self):
            return self.__str__()

    def __init__(self, request, year, day):
        super().__init__(request, year, day)


    def first_problem(self):
        board_h_size = 2000
        board_v_size = 2000
        self.rope = self.Rope(board_v_size, board_h_size, 2)

        for line in self.first_file_lines:
            (command, parameter) = line.split()
            parameter = int(parameter)
            self.rope.move(command, parameter)
        
        return (np.count_nonzero(self.rope.board.board=="#"))

    def second_problem(self):
        board_h_size = 2000
        board_v_size = 2000
        self.rope = self.Rope(board_v_size, board_h_size, 10)

        for line in self.second_file_lines:
            (command, parameter) = line.split()
            parameter = int(parameter)
            self.rope.move(command, parameter)

        return (np.count_nonzero(self.rope.board.board=="#"))


def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())