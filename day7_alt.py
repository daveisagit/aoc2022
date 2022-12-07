""" Day 7 in the AoC house, who are the worm eaters today?
Nick! well done, a defo step up in the difficulty
"""
from collections import namedtuple
from anytree import AnyNode, RenderTree, AsciiStyle, PreOrderIter

from tools.common import file_to_list

lines = file_to_list("day7.txt")

DirObj = namedtuple(
    "DirObj", ["object", "size"]
)


class Dir(AnyNode):

    @property
    def ren(self):
        return f"{self.name} {self.size()}"

    def size(self):
        files = sum(self.files.values())
        dirs = sum([dir.size() for dir in self.children])
        return files + dirs


filesystem = Dir(name="/", files={})
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
                current_dir = [c for c in current_dir.children if c.name == new_cd][0]

        # ls - nothing to actually do until we get the next $
        # up to then the lines are the output from this ls
        if cmd.startswith("ls"):
            pass

    else:

        # read output
        if line.startswith("dir"):
            entry = line[4:]
            if entry not in [n.name for n in current_dir.children]:
                # don't create a new dir object if we have seen it before
                new_dir = Dir(parent=current_dir, name=entry, files={})
        else:
            # the file size should not change if seeing it again? So ok to overwrite
            entry = line.split(" ")
            file_name = entry[1]
            file_size = entry[0]
            current_dir.files[file_name] = int(file_size)


all_dirs = [
    DirObj(
        object=d,
        size=d.size()
    )
    for d in PreOrderIter(filesystem)
]


small_dirs = [dir for dir in all_dirs if dir.size <= 100000]
print("Sum of small ones: ", sum([dir.size for dir in small_dirs]))

free_up = filesystem.size() - 40000000
print("Free up: ", free_up)

dirs_size_asc = sorted(all_dirs, key=lambda d: d.size)
big_enough = [dir for dir in dirs_size_asc if dir.size > free_up]
smallest_big_enough = big_enough[0]
print("Delete :", smallest_big_enough.object, smallest_big_enough.size)

print(RenderTree(filesystem, style=AsciiStyle()).by_attr("ren"))
