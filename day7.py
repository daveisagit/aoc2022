""" Day 7 in the AoC house, who are the worm eaters today?
Nick! well done, a defo step up in the difficulty
"""
from collections import namedtuple

from tools.common import file_to_list

lines = file_to_list("day7.txt")

DirObj = namedtuple(
    "DirObj", ["object", "size"]
)


class Dir:

    def __init__(self, name):
        self.name = name
        self.dirs = {}
        self.files = {}
        self.parent = None

    def size(self):
        files = sum(self.files.values())
        dirs = sum([dir.size() for dir in self.dirs.values()])
        return files + dirs

    def __repr__(self):
        return self.name


filesystem = Dir("/")
current_dir = filesystem

for idx, line in enumerate(lines):

    if line.startswith("$"):

        # command
        cmd = line[2:]

        # cd
        if cmd.startswith("cd"):
            new_cd = cmd[3:]
            if new_cd == "/":
                current_dir = filesystem
            elif new_cd == "..":
                current_dir = current_dir.parent
            else:
                current_dir = current_dir.dirs[new_cd]

        # ls - nothing to actually do until we get the next $
        # up to then the lines are the output from this ls
        if cmd.startswith("ls"):
            pass

    else:

        # read output
        if line.startswith("dir"):
            entry = line[4:]
            if entry not in current_dir.dirs:
                # don't create a new dir object if we have seen it before
                new_dir = Dir(entry)
                new_dir.parent = current_dir
                current_dir.dirs[entry] = new_dir
        else:
            # the file size should not change if seeing it again? So ok to overwrite
            entry = line.split(" ")
            file_name = entry[1]
            file_size = entry[0]
            current_dir.files[file_name] = int(file_size)


def add_to_all_dirs(parent_dir: Dir):
    """create a flat list of all the directories"""
    dir_obj = DirObj(object=parent_dir, size=parent_dir.size())
    all_dirs.append(dir_obj)
    for child in parent_dir.dirs.values():
        add_to_all_dirs(child)


all_dirs = []
add_to_all_dirs(filesystem)

small_dirs = [dir for dir in all_dirs if dir.size <= 100000]
print("Sum of small ones: ", sum([dir.size for dir in small_dirs]))

free_up = filesystem.size() - 40000000
print("Free up: ", free_up)

dirs_size_asc = sorted(all_dirs, key=lambda d: d.size)
big_enough = [dir for dir in dirs_size_asc if dir.size > free_up]
smallest_big_enough = big_enough[0]
print("Delete :", smallest_big_enough.object, smallest_big_enough.size)

