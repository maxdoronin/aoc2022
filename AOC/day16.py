from AOC.Solver import Solver
import re
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.further_init()

    def further_init(self):
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        self.map = dict()
        self.working_valves = dict()
        for line in self.first_file_lines:
            entry = re.findall(r"Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]* lead[s]* to valve[s]* (.+)", line)[0]
            cave = entry[0]
            tunnels = entry[2].split(", ")
            valve = int(entry[1])
            self.map[cave] = {"valve": valve, "tunnels": tunnels}
            if valve > 0:
                self.working_valves[cave] = [valve, 0]

        # pre-calculate distances between all pairs of working valves + "AA"        
        self.distances = dict()
        AA_and_working_valves = ["AA"]+list(self.working_valves.keys())
        for (i, cave_1) in enumerate(AA_and_working_valves):
            for cave_2 in AA_and_working_valves[i+1:]:
                distance = len(self.find_best_path(cave_1, cave_2, []))-1
                self.distances[f"{cave_1}-{cave_2}"] = distance
        
        # split all working valves between me and elephant
        self.my_valve_options = [list(combination) for combination in itertools.combinations((self.working_valves), len(self.working_valves) // 2)]
        self.elephant_valve_options = []
        for my_valves in self.my_valve_options:
            self.elephant_valve_options.append([valve for valve in list(self.working_valves.keys()) if valve not in my_valves])

    def get_accumulated_flow(self, end, start_time, window = 30):
        benefit = (window-start_time)*self.working_valves[end][0]
        return (benefit)

    def find_best_path(self, start, finish, visited):
        visited += [start]
        if finish in self.map[start]["tunnels"]:
            return ([start, finish])
        else:
            candidates = []
            for t in self.map[start]["tunnels"]:
                iter_visited = visited.copy()
                if t in iter_visited:
                    continue
                candidate = self.find_best_path(t, finish, iter_visited)
                if (len(candidate) > 0):
                    candidates.append(candidate)
            candidates.sort(key = lambda x: len(x))
            if len(candidates) == 0:
                return ([])
            else:
                return ([start] + candidates[0])
    
    def get_distance(self, start, end):
        return (self.distances.get(f"{start}-{end}", self.distances.get(f"{end}-{start}", None)))

    def maximize_accumulated_flow(self, start, visited, distance=0, flow=0, window=30, valve_list = None):
        if valve_list == None:
            valve_list = list(self.working_valves.keys())
        flow_increment = 0
        best_branch = visited
        for cave in [cave for cave in valve_list if cave not in visited]:
            visited_copy = visited.copy()
            visited_copy += [cave]
            new_distance = distance + self.get_distance(start, cave) + 1
            if new_distance > window:
                continue
            else:
                current_flow_increment = self.get_accumulated_flow(cave, new_distance, window)
                (branch_flow_increment, branch) = self.maximize_accumulated_flow(cave, visited_copy, new_distance, flow, window, valve_list)
                new_flow_increment = current_flow_increment + branch_flow_increment
                if new_flow_increment > flow_increment:
                    flow_increment = new_flow_increment
                    best_branch = branch
        return (flow_increment, best_branch)

    def first_problem(self):
        result = self.maximize_accumulated_flow("AA", ["AA"])
        return (result)

    def second_problem(self):
        result = 0
        for (i, my_valves) in enumerate(self.my_valve_options):
            elephant_valves = self.elephant_valve_options[i]
            (my_flow, my_path) = self.maximize_accumulated_flow("AA", [], 0, 0, 26, my_valves)
            (elephant_flow, elephant_path) = self.maximize_accumulated_flow("AA", [], 0, 0, 26, elephant_valves)
            if my_flow + elephant_flow > result:
                result = my_flow + elephant_flow
                my_winning_flow = my_flow
                my_winning_path = my_path
                elephant_winning_flow = elephant_flow
                elephant_winning_path = elephant_path
        text_result = f"my_winning_path: {my_winning_path} / {my_winning_flow}, elephant_winning_path: {elephant_winning_path} / {elephant_winning_flow}"
        return (result, text_result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())