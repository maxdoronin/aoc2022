from AOC.Solver import Solver

class DayXSolver(Solver):
    def __init__(self, request):
        super().__init__(request)

    class Stack(object):
        def __init__(self, s: str):
            self.s = s

        def pop(self, count: int):
            if len(self.s) == 0:
                return ("")
            r = self.s[-count:]
            self.s = self.s[:-count]
            return (r)
        
        def push(self, s: str):
            self.s += s
            return(self.s)

        def __str__(self):
            return (self.s)

        def __repr__(self):
            return (self.s)

    def reverse(self, s:str):
        return (s[::-1])

    def parse_input(self, input_lines):
        processing_crates = True
        stacks = []
        stack_count = 0
        moves = list()
        first_line = True

        for line in input_lines:
            if first_line:
                first_line = False
                stack_count=((len(line)+1)//4)
                stacks.extend([""]*(stack_count))
            if processing_crates:
                if len(line) == 0:
                    processing_crates = False
                    continue                    
                elif line[1]=="1":
                    continue
                for stack_index in range(stack_count):
                    if len(line[stack_index*4+1].strip()) == 1:
                        stacks[stack_index] += line[stack_index*4+1]
            else:
                move={"count":0, "from":0, "to":0}
                move_line=line.split()
                move["count"]=int(move_line[1])
                move["from"]=int(move_line[3])
                move["to"]=int(move_line[5])
                moves.append(move)
        
        for i in range(len(stacks)):
            stacks[i] = self.Stack(self.reverse(stacks[i]))

        return(stacks, moves)

    def first_problem(self):
        result=""
        (stacks, moves) = self.parse_input(self.first_file_lines)

        for move in moves:
            stacks[move["to"]-1].push(self.reverse(stacks[move["from"]-1].pop(move["count"])))

        for s in stacks:
            result += s.pop(1)
        return (result)

    def second_problem(self):
        result=""
        (stacks, moves) = self.parse_input(self.second_file_lines)
        for move in moves:
            stacks[move["to"]-1].push(stacks[move["from"]-1].pop(move["count"]))

        for s in stacks:
            result += s.pop(1)
        return (result)

def process(request):
    solver = DayXSolver(request)
    return (solver.process())