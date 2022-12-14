from AOC.Solver import Solver
import numpy as np
from moviepy.editor import ImageSequenceClip


class RC():
    def __init__(self, r=0, c=0, rc=None):
        if rc == None:
            self.r = r
            self.c = c
        else:
            self.r = rc.r
            self.c = rc.c             
    
    def set_pos(self, r, c):
        self.r = r
        self.c = c
    
    def get_pos(self):
        return (self.r, self.c)

    def move(self, dr, dc):
        self.r += dr
        self.c += dc

    def delta_r(self, rc):
        return (rc.r - self.r)

    def delta_c(self, rc):
        return (rc.c - self.c)

    def __eq__(self, other):
        if not isinstance(other, RC):
            return NotImplemented
        return ((self.r == other.r) and (self.c == other.c))

    def __str__(self):
        return (f"(r:{self.r}, c:{self.c})")

    def __repr__(self):
        return self.__str__()

class Board():
    def __init__(self, rows, cols, rocks):
        self.rows = rows+1
        self.cols = cols+1
        self.board = np.chararray((self.rows, self.cols), unicode=True, itemsize=1)
        self.board[:] = "."
        for rock_line in rocks:
            for i in range(len(rock_line) - 1):
                rock_1 = rock_line[i]
                rock_2 = rock_line[i+1]
                delta_r = rock_1.delta_r(rock_2) // max(abs(rock_1.delta_r(rock_2)), 1)
                delta_c = rock_1.delta_c(rock_2) // max(abs(rock_1.delta_c(rock_2)), 1)
                r = RC(rc=rock_1)
                self.set_board_value(r,"#")
                while r != rock_2:
                    r.move(delta_r, delta_c)
                    self.set_board_value(r,"#")                
    
    def get_board_value(self, rc: RC):
        return (self.board[rc.r][rc.c])

    def set_board_value(self, rc: RC, v: str):
        self.board[rc.r][rc.c]=v

    def within_bounds(self, rc):
        return ((0 <= rc.r <= self.rows - 1) and (0 <= rc.c <= self.cols - 1))

    def grain_fall_step(self, rc):
        result = RC(-1, -1)
        options = [RC(rc.r+1, rc.c), RC(rc.r+1, rc.c-1), RC(rc.r+1, rc.c+1)]
        for option in options:
            if not self.within_bounds(option):
                break
            if self.get_board_value(option) in ("#", "o"):
                continue
            result = option
            break
        else:
            result = rc
        return (result)

    def __str__(self):
        return self.board.__str__()
    
    def __repr__(self):
        return self.board.__str__()

class DayXSolver(Solver):

    def __init__(self, request, year, day):
        super().__init__(request, year, day)

    def part_1_init(self):
        rows = 0
        cols = 0
        rocks = []
        for line in self.first_file_lines:
            rock_line = []
            rock_line_c = line.split(" -> ")
            for rock in rock_line_c:
                (c, r) = rock.split(",")
                r = int(r)
                c = int(c)
                rows = max(rows, r)
                cols = max(cols, c)
                rock_line.append(RC(r, c))
            rocks.append(rock_line)
        self.board_1 = Board(rows, cols, rocks)
        return (rows, cols)

    def part_2_init(self):
        rows = 0
        cols = 0
        rocks = []
        for line in self.first_file_lines:
            rock_line = []
            rock_line_c = line.split(" -> ")
            for rock in rock_line_c:
                (c, r) = rock.split(",")
                r = int(r)
                c = int(c)
                rows = max(rows, r)
                cols = max(cols, c)
                rock_line.append(RC(r, c))
            rocks.append(rock_line)
        rows = rows+2
        cols = 500+rows+2
        rocks.append((RC(rows, 0), RC(rows, cols)))
        self.board_2 = Board(rows, cols, rocks)

    def generate_frame(self, offset=450, board=None):
        rows = board.rows
        cols = board.cols
        frame = np.full((rows, cols-offset, 4), 0, dtype=np.uint8)
        for (r, line) in enumerate(board.board):
            for (c, sym) in enumerate (line):
                if c < offset:
                    continue
                if sym == ".":
                    frame[r,c-offset,0] = 0
                    frame[r,c-offset,1] = 0
                    frame[r,c-offset,2] = 0
                if sym == "#":
                    frame[r,c-offset,0] = 64
                    frame[r,c-offset,1] = 64
                    frame[r,c-offset,2] = 64
                if sym == "o":
                    frame[r,c-offset,0] = 200
                    frame[r,c-offset,1] = 200
                    frame[r,c-offset,2] = 200
        return frame

    def first_problem(self):
        frames = []
        result=0
        self.part_1_init()
        source = RC(0,500)

        grain = RC(rc=source)
        step = 0
        while True:
            new_grain = self.board_1.grain_fall_step(grain)
            if grain == new_grain:
                self.board_1.set_board_value(new_grain, "o")
                grain = RC(rc=source)
                result += 1
                if step % 3 == 0:
                    frames.append(self.generate_frame(offset = 450, board=self.board_1))
            elif new_grain == RC(-1, -1):
                break
            else:
                grain = new_grain
            step += 1

        clip = ImageSequenceClip(frames, fps=25)
        clip.write_videofile('part1.mp4', fps=25, codec="libx264")

        return (result)

    def second_problem(self):
        frames = []
        result=0
        self.part_2_init()
        source = RC(0,500)

        grain = RC(rc=source)
        grain_age = 0
        step = 0
        while True:
            new_grain = self.board_2.grain_fall_step(grain)
            if grain == new_grain:
                if (grain_age == 0):
                    break
                self.board_2.set_board_value(new_grain, "o")
                grain = RC(rc=source)
                grain_age = 0
                result += 1
                if step % (10 + result // 500) == 0:
                    frames.append(self.generate_frame(offset = 300, board=self.board_2))
            else:
                grain = new_grain
                grain_age += 1
            step += 1
        clip = ImageSequenceClip(frames, fps=25)
        clip.write_videofile('part2.mp4', fps=25, codec="libx264")
        return (result+1)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())