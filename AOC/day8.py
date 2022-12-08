from AOC.Solver import Solver
import numpy as np

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.forest_size = len(self.first_file_lines)
        self.forest = np.full((self.forest_size, self.forest_size), 0, dtype=np.uint8)
        self.highest_north_tree = np.full((self.forest_size, self.forest_size), 0, dtype=np.uint8)
        self.highest_west_tree = np.full((self.forest_size, self.forest_size), 0, dtype=np.uint8)
        self.highest_south_tree = np.full((self.forest_size, self.forest_size), 0, dtype=np.uint8)
        self.highest_east_tree = np.full((self.forest_size, self.forest_size), 0, dtype=np.uint8)
        for (r, line) in enumerate (self.first_file_lines):
            for (c, sym) in enumerate(line):
                self.forest[r][c] = int(sym)

    def north_tree(self, r, c):
        if r == 0:
            return (0)
        else:
            return (self.forest[r-1][c])

    def west_tree(self, r, c):
        if c == 0:
            return (0)
        else:
            return (self.forest[r][c-1])

    def south_tree(self, r, c):
        if r == self.forest_size-1:
            return (0)
        else:
            return (self.forest[r+1][c])

    def east_tree(self, r, c):
        if c == self.forest_size-1:
            return (0)
        else:
            return (self.forest[r][c+1])

    def highest_north_tree_here(self, r, c):
        if r == 0:
            return (0)
        else:
            return (max(self.highest_north_tree[r-1][c], self.north_tree(r, c)))

    def highest_west_tree_here(self, r, c):
        if c == 0:
            return (0)
        else:
            return (max(self.highest_west_tree[r][c-1], self.west_tree(r, c)))

    def highest_south_tree_here(self, r, c):
        if r == self.forest_size-1:
            return (0)
        else:
            return (max(self.highest_south_tree[r+1][c], self.south_tree(r, c)))

    def highest_east_tree_here(self, r, c):
        if c == self.forest_size-1:
            return (0)
        else:
            return (max(self.highest_east_tree[r][c+1], self.east_tree(r, c)))

    def generate_visibility_maps(self):
        for r in range(self.forest_size):
            for c in range(self.forest_size):
                if r > 0:
                    self.highest_north_tree[r][c] = self.highest_north_tree_here(r, c)
                if c > 0:
                    self.highest_west_tree[r][c] = self.highest_west_tree_here(r, c)
        for r in range(self.forest_size - 1, -1, -1):
            for c in range(self.forest_size - 1, -1, -1):
                if r < self.forest_size - 1:
                    self.highest_south_tree[r][c] = self.highest_south_tree_here(r, c)
                if c < self.forest_size - 1:
                    self.highest_east_tree[r][c] = self.highest_east_tree_here(r, c)

    def count_visible_trees(self):
        result=0
        for r in range(self.forest_size):
            for c in range(self.forest_size):
                tree = self.forest[r,c]
                if (r == 0 or c == 0 or
                    r == self.forest_size - 1 or c == self.forest_size - 1 or
                    tree > self.highest_north_tree[r][c] or
                    tree > self.highest_west_tree[r][c] or
                    tree > self.highest_south_tree[r][c] or
                    tree > self.highest_east_tree[r][c]):
                    result += 1
        return (result)

    def calculate_scenic_score(self, r, c):
        tree = self.forest[r][c]
        north_scenic_score = 0
        west_scenic_score = 0
        south_scenic_score = 0
        east_scenic_score = 0
        print (f"tree: {tree}")
        for i in range(r-1, -1, -1):
            north_scenic_score += 1
            if tree <= self.forest[i][c]:
                break
        for j in range(c-1, -1, -1):
            west_scenic_score += 1
            if tree <= self.forest[r][j]:
                break
        for i in range(r+1, self.forest_size):
            south_scenic_score += 1
            if tree <= self.forest[i][c]:
                break
        for j in range(c+1, self.forest_size):
            east_scenic_score += 1
            if tree <= self.forest[r][j]:
                break
        scenic_score = north_scenic_score * south_scenic_score * east_scenic_score * west_scenic_score
        return (scenic_score)
        

    def first_problem(self):
        result=0
        self.generate_visibility_maps()
        result = self.count_visible_trees()
        return (result)

    def second_problem(self):
        result = 0
        for r in range(1, self.forest_size):
            for c in range(1, self.forest_size):
                result = max(result, self.calculate_scenic_score(r, c))
        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())