from AOC.Solver import Solver
import numpy as np

class DayXSolver(Solver):
    class Map():
        class RC():
            def __init__(self, r, c):
                self.r = r
                self.c = c
            
            def set_pos(self, r, c):
                self.r = r
                self.c = c
            
            def up(self):
                return (self.__class__(self.r-1, self.c))

            def down(self):
                return (self.__class__(self.r+1, self.c))

            def left(self):
                return (self.__class__(self.r, self.c-1))

            def right(self):
                return (self.__class__(self.r, self.c+1))

            def get_pos(self):
                return (self.r, self.c)
            
            def __str__(self):
                return (f"(r:{self.r}, c:{self.c})")

            def __repr__(self):
                return self.__str__()

        def __init__(self, v_size=1, h_size=1, val=0):
            self.v_size = v_size
            self.h_szie = h_size
            self.map = np.full((v_size, h_size), val, dtype=np.int16)

        def set_point(self, rc, value):
            self.map[rc.r, rc.c] = value

        def get_point(self, rc):
            return (self.map[rc.r, rc.c])

    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.map_v_size = len(self.first_file_lines)
        self.map_h_size = len(self.first_file_lines[0])
        self.map = self.Map(self.map_v_size, self.map_h_size)
        self.distances = self.Map(self.map_v_size, self.map_h_size, val=2**16//2-1)
        self.visited = self.Map(self.map_v_size, self.map_h_size)
        for (r, line) in enumerate(self.first_file_lines):
            for (c, sym) in enumerate(line):
                rc = self.Map.RC(r, c)
                if sym == "S":
                    self.start = rc
                    sym = "a"
                elif sym == "E":
                    self.end = rc
                    sym = "z"
                    self.distances.set_point(rc, 0)
                    self.visited.set_point(rc, 1)
                self.map.set_point(rc, ord(sym) - ord("a"))

    def check_candidates_reverse(self, rc):
        candidates = []
        distance_rc = self.distances.get_point(rc)
        if rc.r > 0:
            up = rc.up()
            if  (self.visited.get_point(up) == 0 and
            self.map.get_point(rc) - self.map.get_point(up) <= 1 and
            self.distances.get_point(up) > distance_rc + 1):
                self.distances.set_point(up, distance_rc + 1)
                candidates.append(up)
        if rc.r < self.map_v_size - 1:
            down = rc.down()
            if (self.visited.get_point(down) == 0 and
            self.map.get_point(rc) - self.map.get_point(down) <= 1
            and self.distances.get_point(down) > distance_rc + 1):
                self.distances.set_point(down, distance_rc + 1)
                candidates.append(down)
        if rc.c > 0:
            left = rc.left()
            if (self.visited.get_point(left) == 0 and
            self.map.get_point(rc) - self.map.get_point(left) <= 1 and
            self.distances.get_point(left) > distance_rc + 1):
                self.distances.set_point(left, distance_rc + 1)
                candidates.append(left)
        if rc.c < self.map_h_size-1:
            right = rc.right()
            if (self.visited.get_point(right) == 0 and
            self.map.get_point(rc) - self.map.get_point(right) <= 1 and
            self.distances.get_point(right) > distance_rc + 1):
                self.distances.set_point(right, distance_rc + 1)
                candidates.append(right)
                
        return(candidates)

    def map_distances_reverse(self, rc):
        candidates = self.check_candidates_reverse(rc)
        if len(candidates) == 0:
            return
        for candidate in candidates:
            self.map_distances_reverse(candidate)

    def first_problem(self):        
        print (self.map.map)
        self.map_distances_reverse(self.end)
        return (self.distances.get_point(self.start))

    def second_problem(self):
        min_distance = 2**16//2-1
        for r in range(self.distances.map.shape[0]):
            for c in range(self.distances.map.shape[1]):
                if self.map.get_point(self.Map.RC(r,c)) == 0:
                    min_distance = min(self.distances.get_point(self.Map.RC(r,c)), min_distance)
        return (min_distance)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())