""" Day 6 in the AoC house and James ups his game taking pole place before 6:30am
Nick wipes his morning eyes to see 3 leaders with 6 starts already, WTF!!"""

from tools.common import file_to_string, unique_characters, window_over_string


def find_window_of_unique_characters(text: str, width: int) -> int | None:
    """Returns the index of the first window of unique characters"""
    for idx, packet in enumerate(window_over_string(text, width)):
        if len(unique_characters(packet)) == width:
            return idx
    return None


content = file_to_string("day6.txt")

# Example (otherwise I will no doubt be 1 out from some vexing & perplexing indexing)

# For aaabcdefg, abcd starting at 2, ending at 5 is the packet
# we want to report the end of the marker which is d at 5
# but the puzzle index has base=1, so we add 1 giving 6 as the answer
# So the answer = start of window + width
print("A: ", find_window_of_unique_characters(content, 4) + 4)
print("B: ", find_window_of_unique_characters(content, 14) + 14)

