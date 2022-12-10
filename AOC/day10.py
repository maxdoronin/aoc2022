from AOC.Solver import Solver

class DayXSolver(Solver):
    def first_problem(self):
        result=0
        command_len = {"noop": 1, "addx": 2}
        next_measurement_cycle = 20
        measurement_increment = 40
        cycle = 0
        reg_value = 1

        for line in self.first_file_lines:
            if line.startswith("addx"):
                (command, param) = line.split()
            else:
                command = line.strip()
                param = 0

            if cycle + command_len[command] >= next_measurement_cycle:
                result += reg_value*next_measurement_cycle
                next_measurement_cycle += measurement_increment

            if command == "addx":
                param = int(param)
                reg_value += param
            cycle += command_len[command]

        return (result)

    def second_problem(self):
        command_len = {"noop": 1, "addx": 2}
        reg_value = 1
        crt = ["","","","","",""]
        ray_h_pos = 0
        crt_h_res = 40
        crt_v_res = 6

        lines = iter(self.first_file_lines)
        line = next(lines)
        if line.startswith("addx"):
            (command, param) = line.split()
        else:
            command = line.strip()
            param = 0
        command_pending = command_len[command]       

        for i in range(crt_h_res*crt_v_res):
            ray_h_pos = i % crt_h_res
            ray_v_pos = i // crt_h_res
            command_pending += -1
            if reg_value - 1 <= ray_h_pos <= reg_value + 1:
                crt[ray_v_pos] += "#"
            else:
                crt[ray_v_pos] += "."

            if command_pending == 0:
                if command == "addx":
                    param = int(param)
                    reg_value += param
                try:
                    line = next(lines)
                except:
                    line = "noop"
                if line.startswith("addx"):
                    (command, param) = line.split()
                else:
                    command = line.strip()
                    param = 0
                command_pending = command_len[command]
        return ("\n".join(crt))

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())