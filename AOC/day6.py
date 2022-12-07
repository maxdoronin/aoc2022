from AOC.Solver import Solver

class DayXSolver(Solver):
    def locate_start_marker(self, message: str, sequence_length: int):
        symbol_buffer=""
        for (n, symbol) in enumerate(message):
            if len(symbol_buffer) < sequence_length:
                if symbol in symbol_buffer:
                    symbol_buffer = symbol_buffer[symbol_buffer.find(symbol)+1:]
                symbol_buffer += symbol
            else:
                return (n)

    def first_problem(self):
        line = next(iter(self.first_file_lines), None)
        return (self.locate_start_marker(line, 4))

    def second_problem(self):
        line = next(iter(self.second_file_lines), None)
        return (self.locate_start_marker(line, 14))

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())