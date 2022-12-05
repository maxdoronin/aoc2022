from AOC.Solver import Solver

class DayXSolver(Solver):
    def __init__(self, request):
        super().__init__(request)

    class Stack:
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

    class CraneCommand:
        def __init__(self, s: str):
            command = s.split()
            self.count = int(command[1])
            self.src = int(command[3])-1
            self.dst = int(command[5])-1
        
        def __str__(self):
            return (f"<count: {self.count}, from: {self.src}, to: {self.dst}>")

        def __repr__(self):
            return (self.__str__())

    def reverse(self, s:str):
        return (s[::-1])

    def parse_input(self, input_lines):
        processing_crates = True
        stack_strings = []
        stacks = []
        stack_count = 0
        commands = list()
        first_line = True

        for line in input_lines:
            if first_line:
                first_line = False
                stack_count=((len(line)+1)//4)
                stack_strings.extend([""]*stack_count)
            if processing_crates:
                if len(line) == 0:
                    processing_crates = False
                    continue                    
                elif line[1]=="1":
                    continue
                for stack_index in range(stack_count):
                    crate = line[stack_index*4+1].strip()
                    if len(crate) == 1:
                        stack_strings[stack_index] += crate
            else:
                command=self.CraneCommand(line)
                commands.append(command)
        
        for i in range(stack_count):
            stacks.append(self.Stack(self.reverse(stack_strings[i])))

        return(stacks, commands)

    def first_problem(self):
        result=""
        (stacks, commands) = self.parse_input(self.first_file_lines)

        for command in commands:
            stacks[command.dst].push(self.reverse(stacks[command.src].pop(command.count)))

        for s in stacks:
            result += s.pop(1)
        return (result)

    def second_problem(self):
        result=""
        (stacks, commands) = self.parse_input(self.second_file_lines)
        for command in commands:
            stacks[command.dst].push(stacks[command.src].pop(command.count))

        for s in stacks:
            result += s.pop(1)
        return (result)

def process(request):
    solver = DayXSolver(request)
    return (solver.process())