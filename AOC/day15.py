from AOC.Solver import Solver
import re

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year,day)

        self.sensors = []
        for line in self.first_file_lines:
            coords = re.findall(r"[-]*\d+", line)
            s = (int(coords[0]), int(coords[1]))
            b = (int(coords[2]), int(coords[3]))
            self.sensors.append((s, b))

    def first_problem(self):
        result=0
        target_line = 2000000
        covered_ranges = []
        sensors_in_the_line = set()

        for sensor in self.sensors:
            if sensor[1][1] == target_line:
                sensors_in_the_line.add((sensor[1][1], sensor[1][1]))
            radius = abs(sensor[1][0] - sensor[0][0]) + abs(sensor[1][1] - sensor[0][1])
            l = radius - abs(sensor[0][1] - target_line)
            if l >= 0:
                x1 = sensor[0][0] - l
                x2 = sensor[0][0] + l
                covered_ranges.append((x1, x2))
        covered_ranges += sensors_in_the_line
        covered_ranges = sorted(covered_ranges, key=lambda x: x[0])

        result_ranges = []
        r1 = covered_ranges.pop(0)
        while len(covered_ranges) > 0:
            r2 = covered_ranges.pop(0)
            if (r2[0]-r1[1]>1):
                result_ranges.append(r1)
                r1 = r2
            else:
                r1 = (r1[0], max(r1[1], r2[1]))
        result_ranges.append(r1)
        for r in result_ranges:
            result += r[1]-r[0]
        return (result)

    def second_problem(self):
        result = 0
        max_coord = 4000000

        for target_line in range(max_coord+1):
            covered_ranges = []
            sensors_in_the_line = set()

            for sensor in self.sensors:
                if sensor[1][1] == target_line:
                    sensors_in_the_line.add((sensor[1][1], sensor[1][1]))
                radius = abs(sensor[1][0] - sensor[0][0]) + abs(sensor[1][1] - sensor[0][1])
                l = radius - abs(sensor[0][1] - target_line)
                if l >= 0:
                    x1 = sensor[0][0] - l
                    x2 = sensor[0][0] + l
                    x1 = max (x1, 0)
                    x2 = min (x2, max_coord)
                    if x2 < x1:
                        continue
                    covered_ranges.append((x1, x2))
            covered_ranges += sensors_in_the_line
            covered_ranges = sorted(covered_ranges, key=lambda x: x[0])

            r1 = covered_ranges.pop(0)
            while len(covered_ranges) > 0:
                r2 = covered_ranges.pop(0)                  
                if (r2[0]-r1[1]>1):
                    result = target_line + 4000000*(r1[1]+1)
                    break
                else:
                    r1 = (r1[0], max(r1[1], r2[1]))

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())