from AOC.Solver import Solver
import re

class DayXSolver(Solver):
    class Monkey():
        def __init__(self, monkey_lines):
            self.inspected_count = 0
            self.monkey_index = re.findall(r'\d+', monkey_lines[0])[0]
            self.items = re.findall(r'\d+', monkey_lines[1])
            items = [int(x) for x in self.items]
            self.items = items
            self.op = re.findall(r'\+|\*', monkey_lines[2])[0]
            self.op_arg = monkey_lines[2].split()[-1:][0]
            try:
                op_arg = int(self.op_arg)
            except:
                op_arg = "old"
            self.op_arg = op_arg
            self.test_arg = int(re.findall(r'\d+', monkey_lines[3])[0])
            self.target_if_true = int(re.findall(r'\d+', monkey_lines[4])[0])
            self.target_if_false = int(re.findall(r'\d+', monkey_lines[5])[0])

        def play_part_1(self, manage_worry_level: callable):
            res = {self.target_if_true: [], self.target_if_false: []}

            def mul(a, b):
                return (a*b)
            def add(a, b):
                return (a+b)
            funcs = {"*": mul, "+": add}

            for item_index in range(len(self.items)):
                self.inspected_count += 1
                item = self.items[item_index]
                op_arg = self.op_arg
                if self.op_arg == "old":
                    op_arg = item
                item = funcs[self.op](item, op_arg)
                item = manage_worry_level(item)
                if item % self.test_arg == 0:
                    res[self.target_if_true].append(item)
                else:
                    res[self.target_if_false].append(item)
            self.items = []
            return (res)

        def play_part_2(self, manage_worry_level: callable):
            res = {self.target_if_true: [], self.target_if_false: []}

            def mul(a, b):
                return (a*b)
            def add(a, b):
                return (a+b)
            funcs = {"*": mul, "+": add}

            for item_index in range(len(self.items)):
                self.inspected_count += 1
                item = self.items[item_index]
                op_arg = self.op_arg
                if self.op_arg == "old":
                    op_arg = item
                item = funcs[self.op](item, op_arg)
                item = manage_worry_level(item)

                if item % self.test_arg == 0:
                    res[self.target_if_true].append(item)
                else:
                    res[self.target_if_false].append(item)
            self.items = []
            return (res)
        
        def catch_items(self, items):
            self.items += items
        
        def __str__(self):
            attributes = vars(self)
            return ("\n".join ("%s: %s" % item for item in attributes.items()))

        def __repr__(self):
            return (self.__str__())

    def parse_input(self, input):
        self.monkeys=[]
        while len(input) > 0:
            monkey_lines = input[0:6]
            input = input[7:]
            self.monkeys.append(self.Monkey(monkey_lines))

    def manage_worry_level_part_1(self, worry_level):
        return (worry_level // self.worry_management_arg)

    def manage_worry_level_part_2(self, worry_level):
        return (worry_level % self.worry_management_arg)
        
    def first_problem(self):
        self.worry_management_arg = 3
        self.parse_input(self.first_file_lines)
        for i in range(20):
            for m in self.monkeys:
                play_res = m.play_part_1(self.manage_worry_level_part_1)
                for key in play_res.keys():
                    self.monkeys[key].catch_items(play_res[key])
        
        inspected_counters = [m.inspected_count for m in self.monkeys]
        max1 = max(inspected_counters)
        inspected_counters.remove(max1)
        max2 = max(inspected_counters)

        return (max1*max2)

    def second_problem(self):
        self.parse_input(self.second_file_lines)
        self.worry_management_arg = 1
        for m in self.monkeys:
            self.worry_management_arg *= m.test_arg
 
        for i in range(10000):
            for m in self.monkeys:
                play_res = m.play_part_2(self.manage_worry_level_part_2)
                for key in play_res.keys():
                    self.monkeys[key].catch_items(play_res[key])
        
        inspected_counters = [m.inspected_count for m in self.monkeys]
        max1 = max(inspected_counters)
        inspected_counters.remove(max1)
        max2 = max(inspected_counters)
        return (max1*max2)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())