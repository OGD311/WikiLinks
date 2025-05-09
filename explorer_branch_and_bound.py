from searchQueue import searchQueue
from node import Node
from function_timer import timer

@timer
def branch_and_bound(start_title, goal_title, depth=2):
    queue = searchQueue()
    visited = set()

    queue.enqueue([start_title])

    while not queue.is_empty():
        current_path = queue.dequeue()
        current_title = current_path[-1]

        if len(current_path) > depth:
            continue

        if current_title in visited:
            continue
        visited.add(current_title)

        try:
            current_node = Node(current_title)
        except SyntaxError as e:
            print(e)
            continue

        if current_node.node_in_links(goal_title):
            return current_path + [goal_title]

        for link in current_node.get_links():
            if link not in visited:
                new_path = current_path + [link]
                queue.enqueue(new_path)

        if queue.is_empty() and len(current_path) <= max_depth:
            max_depth *= 2 

    return None

path = branch_and_bound("Amsterdam", "Asia")
if path:
    print("Path found:", " -> ".join(path))
else:
    print("No path found.")

