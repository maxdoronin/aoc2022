from AOC.Solver import Solver

class DayXSolver(Solver):
    def first_problem(self):
        result = 0
        current_elf_calories = 0
        for line in self.first_file_lines:
            if len(line) == 0:
                if current_elf_calories > result:
                    result = current_elf_calories
                current_elf_calories = 0
            else:
                current_elf_calories += int(line)

        if current_elf_calories > result:
            result = current_elf_calories
        return (result)

    def second_problem(self):
        calories = [0, 0, 0]
        current_elf_calories = 0

        for line in self.second_file_lines:
            if len(line) == 0:
                minCalories = min(calories)
                if current_elf_calories > minCalories:
                    minIndex = calories.index(minCalories)
                    calories.pop(minIndex)
                    calories.append(current_elf_calories)
                current_elf_calories = 0
            else:
                current_elf_calories += int(line)

        minCalories = min(calories)
        if current_elf_calories > minCalories:
            minIndex = calories.index(minCalories)
            calories.pop(minIndex)
            calories.append(current_elf_calories)
            
        return (sum(calories))

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())