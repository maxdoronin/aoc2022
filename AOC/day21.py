from AOC.Solver import Solver
import pprint

pp = pprint.PrettyPrinter(indent=4)

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        super().__init__(request, year, day)
        self.further_init()

    def further_init(self):
        self.ops = {"+": self.plus, "-": self.minus, "*": self.mul, "/": self.div, "=": self.equal}
        self.reverse_ops = {"+": self.minus, "-": self.plus, "*": self.div, "/": self.mul}
        self.other_param = {"param_1": "param_2", "param_2": "param_1"}
        self.monkeys = {}
        for l in self.first_file_lines:
            (var, val_str) = l.split(":")
            self.monkeys[var] = {}
            try:
                val_type = "leaf"
                val = int(val_str)
                self.monkeys[var]["val"] = val 
            except:
                val_type = "node"
                (param_1, oper, param_2) = val_str.strip().split()
                self.monkeys[var]["param_1"] = param_1
                self.monkeys[var]["param_2"] = param_2
                self.monkeys[var]["oper"] = oper
            self.monkeys[var]["type"] = val_type

    def init_part_2(self):
        self.monkeys["root"]["oper"] = "="

    def plus(self, a, b):
        return a +b

    def minus(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a // b
    
    def equal(self, a, b):
        return a == b
    
    def solve_monkey(self, monkey="root"):
        node = self.monkeys[monkey]
        if node["type"] == "leaf":
            return node["val"]
        else:
            return self.ops[node["oper"]](self.solve_monkey(node["param_1"]), self.solve_monkey(node["param_2"]))

    def solve_monkey_part_2(self, monkey="root", path=""):
        node = self.monkeys[monkey]
        path += f"/{monkey}"
        if node["type"] == "leaf":
            if monkey != "humn":
                return node["val"]
            else:
                target = 0
                p  = path.split("/")
                root =  self.monkeys["root"]
                (root, param) = p[1].split("+")
                other_sub_root = self.monkeys[root][self.other_param[param]]
                target = self.solve_monkey_part_2(other_sub_root)
                for i in range (2, len(p)-1):
                    (current_monkey, param) = p[i].split("+")
                    if self.monkeys[current_monkey]["oper"] in ["+", "*"]:
                        oper_func = self.reverse_ops[self.monkeys[current_monkey]["oper"]]
                        target = oper_func(target, self.solve_monkey_part_2(self.monkeys[current_monkey][self.other_param[param]]))
                    elif self.monkeys[current_monkey]["oper"] in ["-", "/"]:
                        if param == "param_1":
                            oper_func = self.reverse_ops[self.monkeys[current_monkey]["oper"]]
                            target = oper_func(target, self.solve_monkey_part_2(self.monkeys[current_monkey][self.other_param[param]]))    
                        if param == "param_2":
                            oper_func = self.ops[self.monkeys[current_monkey]["oper"]]
                            target = oper_func(self.solve_monkey_part_2(self.monkeys[current_monkey][self.other_param[param]]), target)
                self.answer_part_2 = target
                return (target)
        else:
            return self.ops[node["oper"]](self.solve_monkey_part_2(node["param_1"], path+f"+param_1"), self.solve_monkey_part_2(node["param_2"], path+f"+param_2"))
    def first_problem(self):
        result=0
        result = self.solve_monkey()

        return (result)

    def second_problem(self):
        self.init_part_2()
        if (self.solve_monkey_part_2()):
            return (self.answer_part_2)
        else:
            return ("We shouldn't be here!")

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())