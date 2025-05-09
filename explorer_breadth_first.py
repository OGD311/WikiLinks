from searchQueue import searchQueue
from node import Node
from function_timer import timer

@timer
def breadth_first(start_title, goal_title):
    queue = searchQueue()
    visited = set()

    queue.enqueue([start_title])

    while not queue.is_empty():
        current_path = queue.dequeue()
        current_title = current_path[-1]

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

    return None

if __name__ == "__main__":
    path = breadth_first("Amsterdam", "Asia")
    if path:
        print("Path found:", " -> ".join(path))
    else:
        print("No path found.")


