from AOC.Solver import Solver
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)
np.set_printoptions(threshold=100)

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.further_init()

    def further_init(self):
        self.droplets = [[int(coord) for coord in line.split(",")] for line in self.first_file_lines]
        self.droplet_count = len(self.droplets)
        self.max_x = max (d[0] for d in self.droplets)
        self.max_y = max (d[1] for d in self.droplets)
        self.max_z = max (d[2] for d in self.droplets)    
        self.air = {}
        for x, y, z in [(x, y, z) for x in range(self.max_x + 1) for y in range(self.max_y + 1) for z in range(self.max_z + 1)]:
            if [x,y,z] not in self.droplets:
                self.air[(x,y,z)] = 0
        self.part_1_answer = 0 
  

    def get_connected_sides_list(self, positions: list):
        sorted_x = sorted(positions, key = lambda x: x[0])
        sorted_y = sorted(positions, key = lambda x: x[1])
        sorted_z = sorted(positions, key = lambda x: x[2])
        sorted_positions = [sorted_x, sorted_y, sorted_z]
        connected_sides_list = []
        position_count = len(positions)

        for i in range (position_count):
            connected_sides_vector = [0, 0, 0]
            for (coord_no, position) in enumerate(sorted_positions):
                current_position = position[i].copy()
                current_position_key_coord = current_position.pop(coord_no)
                j = i - 1
                while j >= 0:
                    left_position = position[j].copy()
                    left_position_key_coord = left_position.pop(coord_no)
                    if abs(current_position_key_coord - left_position_key_coord) > 1:
                        break
                    if current_position == left_position:
                        connected_sides_vector[coord_no] += 1
                        break
                    j -= 1

                current_position = position[i].copy()
                current_position_key_coord = current_position.pop(coord_no)
                j = i + 1
                while j < position_count:
                    right_position = position[j].copy()
                    right_position_key_coord = right_position.pop(coord_no)
                    if abs(right_position_key_coord - current_position_key_coord) > 1:
                        break
                    if current_position == right_position:
                        connected_sides_vector[coord_no] += 1
                        break
                    j += 1
            connected_sides_list.append(connected_sides_vector)

        return (connected_sides_list)

    def propagate_steam_from_point(self, t, air):
        r = self.air.get(t, None)
        stack = []
        if r == 0:
            air[t] = 1
        elif r == None:
            return (stack)

        for neighbour in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            t1 = tuple(map(lambda t, t1: t + t1, t, neighbour))
            if 0 <= t1[0] <= self.max_x and 0 <= t1[1] <= self.max_y and 0 <= t1[2] <= self.max_z:
                r = self.air.get(t1, None)
                if r == 0:
                    air[t1] = 1
                    stack.append(t1)
        return (stack)

    def propagate_steam(self, air):
        stack = []
        z = 0
        for x, y in [(x, y) for x in range(self.max_x + 1) for y in range(self.max_y + 1)]:
            t = (x, y, z)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

        y = 0
        for x, z in [(x, z) for x in range(self.max_x + 1) for z in range(self.max_z + 1)]:
            t = (x, y, z)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

        x = 0
        for y, z in [(y, z) for y in range(self.max_y + 1) for z in range(self.max_z + 1)]:
            t = (x, y, z)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

        z = self.max_z
        for x, y in [(x, y) for x in range(self.max_x + 1) for y in range(self.max_y + 1)]:
            t = (x, y, z)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

        y = self.max_y
        for x, z in [(x, z) for x in range(self.max_x + 1) for z in range(self.max_z + 1)]:
            t = (x, y, z)
            print (t)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

        x = self.max_x
        for y, z in [(y, z) for y in range(self.max_y + 1) for z in range(self.max_z + 1)]:
            t = (x, y, z)
            stack += self.propagate_steam_from_point(t, air)
            while len(stack) > 0:
                tn = stack.pop()
                stack += self.propagate_steam_from_point(tn, air)

    def first_problem(self):
        result=0
        connected_sides = self.get_connected_sides_list(self.droplets)
        for connected_sides_vector in connected_sides:
            result += 6 - sum(connected_sides_vector)
        self.part_1_answer = result
        return (result)

    def second_problem(self):
        self.propagate_steam(self.air)
        trapped_air = [list(position) for position in self.air.keys() if self.air[position] == 0]
        connected_sides = self.get_connected_sides_list(trapped_air)
        pp.pprint(trapped_air)
        print (self.max_x, self.max_y, self.max_z)
        connected = 0
        for connected_sides_vector in connected_sides:
            connected += 6 - sum(connected_sides_vector)    
        print (connected)    

        return (self.part_1_answer - connected)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())