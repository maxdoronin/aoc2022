from AOC.Solver import Solver

class DayXSolver(Solver):
    def letter_value(self, letter):
        if letter.isupper():
            return (ord(letter) - ord("A") + 1 + 26)
        else:
            return (ord(letter) - ord("a") + 1)

    def first_problem(self):
        result=0

        for rucksack in self.first_file_lines:
            compartment_1 = rucksack[:len(rucksack)//2]
            compartment_2 = rucksack[len(rucksack)//2:]

            checked_items = set()
            overlapping_items = set()

            for item in compartment_1:
                if item not in checked_items:
                    checked_items.add(item)
                    if (item not in overlapping_items) and (item in compartment_2):
                        overlapping_items.add(item)
            
            for item in overlapping_items:
                result += self.letter_value(item)

        return (result)

    def second_problem(self):
        result = 0

        badges = list()
        lines = iter(self.second_file_lines)
        while (rucksack_1 := next(lines, None)) is not None:
            # assume the number of rucksacks is always 3n
            # convert to set for O(1) search
            rucksack_1 = set(rucksack_1)
            rucksack_2 = set(next(lines))
            rucksack_3 = set(next(lines))

            for item in rucksack_1:
                if item in rucksack_2 and item in rucksack_3:
                    badges.append(item)
                    break

        for item in badges:
            result += self.letter_value(item)

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())