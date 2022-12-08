from AOC.Solver import Solver

class DayXSolver(Solver):
    def __init__(self, request, year, day):
        self.total_file_size = 0
        self.answer1 = 0
        self.dir_sizes = []
        self.dirs = []
        super().__init__(request, year, day)

    def process_directory(self, lines):
        dirs = []
        if len(lines) == 0:
            return ([],[])
        while True:
            if len(lines) > 0:
                line = lines.pop(0)
            else:
                break
            split_line = line.split()
            if split_line[0] == "$":
                if split_line[1] == "cd":
                    if split_line[2] != "..":
                        (lines, dirs_t) = self.process_directory(lines)
                        dirs.append(dirs_t)
                        continue
                    else:
                        break
                if split_line[1] == "ls":
                    continue
            elif split_line[0] == "dir":
                continue
            else:
                fsize = int(split_line[0])
                self.total_file_size += fsize
                dirs.append(fsize)
                continue

        return (lines, dirs)

    def filter_subdirs_less_than_threshold(self, sizes, threshold):
        sum_files = 0
        sum_subdirs = 0
        for i in sizes:
            if type(i) is int:
                sum_files += i
            else:
                r = self.filter_subdirs_less_than_threshold(i, threshold)
                sum_subdirs += r
        if sum_files + sum_subdirs <= threshold:
            self.answer1 += sum_files + sum_subdirs
        else:
            pass
        return (sum_files + sum_subdirs)

    def size_of_dir_to_delete(self, sizes):
        sum_files = 0
        sum_subdirs = 0
        for i in sizes:
            if type(i) is int:
                sum_files += i
            else:
                sum_subdirs += self.size_of_dir_to_delete(i)
        dir_size = sum_files + sum_subdirs
        self.dir_sizes.append(dir_size)
        return (dir_size)

    def first_problem(self):
        lines = []
        for line in self.first_file_lines:
            lines.append(line)

        lines.pop(0)
        (lines, d) = self.process_directory(lines)
        self.dirs = d

        self.filter_subdirs_less_than_threshold(d, 100000)

        return (self.answer1)

    def second_problem(self):
        storage_size = 70000000
        upgrade_size = 30000000
        current_free_space = storage_size - self.total_file_size
        target_directory_size = upgrade_size - current_free_space
        self.size_of_dir_to_delete(self.dirs)
        result = min([dir_size for dir_size in self.dir_sizes if dir_size >= target_directory_size])

        return (result)

def process(request, year, day):
    solver = DayXSolver(request, year, day)
    return (solver.process())