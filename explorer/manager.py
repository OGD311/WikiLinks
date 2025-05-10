import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from branch_and_bound import branch_and_bound
from iddfs import IDDFS
from breadth_first import breadth_first

start = input("Start: ")
end = input("End: ")
option = int(input("(BFS/Branch and Bound/IDDFS): "))

match(option):
    case 0:
        path = breadth_first(start, end)
    case 1:
        path = branch_and_bound(start, end)
    case 2:
        path = IDDFS(start, end, 3)

    case _:
        path = breadth_first(start, end)

print("Path found: " + " -> ".join(path) if path else "No Path")

