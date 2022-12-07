import os
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> str:
    filepath = os.path.join(input_dir, filename)
    return Path(filepath).read_text().strip().split("\n")


class File:
    def __init__(self, size: str, name: str):
        self.name = name
        self.size = int(size)


class Dir:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.size = 0
        self.files: list[File] = []
        self.dirs: list[Dir] = []

    def add_file(self, file: File):
        self.files.append(file)
        self.update_size(file.size)

    def add_dir(self, dir: "Dir"):
        dir.parent = self
        self.dirs.append(dir)

    def chdir(self, dirname: str):
        for dir in self.dirs:
            if dir.name == dirname:
                return dir
        return None

    def update_size(self, size):
        self.size += size
        if self.parent:
            self.parent.update_size(size)

    def get_dirs(self) -> list["Dir"]:
        dirs = []
        for dir in self.dirs:
            dirs.append(dir)
            dirs.extend(dir.get_dirs())
        return dirs


def build_fs(term: list[str]) -> Dir:
    root = Dir("/")
    cur: Dir = None

    for line in term:
        if line.startswith("$"):
            command = line.split(" ")
            if command[1] == "cd":
                if command[2] == "/":
                    cur = root
                elif command[2] == "..":
                    cur = cur.parent
                else:
                    cur = cur.chdir(command[2])
        else:
            entry = line.split(" ")
            if entry[0] == "dir":
                cur.add_dir(Dir(entry[1]))
            else:
                cur.add_file(File(*entry))
    return root


def part_1(input: list[str]) -> int:
    root = build_fs(input)
    dirs = root.get_dirs()
    return sum([s.size for s in dirs if s.size <= 100000])


NEED = 30000000
TOTAL = 70000000


def part_2(code: str) -> int:
    root = build_fs(input)
    dirs = root.get_dirs()
    unused = TOTAL - root.size
    needed = NEED - unused
    delete_dir = root
    for dir in dirs:
        if dir.size >= needed:
            delete_dir = min(delete_dir, dir, key=lambda x: x.size)
    return delete_dir.size


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
