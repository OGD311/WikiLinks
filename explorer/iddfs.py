from dataStructures import Node, searchQueue
from function_timer import timer

@timer
def IDDFS(start_title, goal_title, depth=2):
    queue = searchQueue()
    nextQueue = searchQueue()
    visited = set()

    queue.enqueue([start_title])

    while not queue.is_empty():
        current_path = queue.dequeue()
        current_title = current_path[-1]

        if len(current_path) == depth:
            nextQueue.enqueue(current_title)

        if len(current_path) > depth:
            continue

        if queue.is_empty() and len(current_path) <= depth:
            print(nextQueue.peek())
            depth *= 2 
            while not nextQueue.is_empty():
                title = nextQueue.dequeue()
                queue.enqueue([title])

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
    path = IDDFS("Amsterdam", "Asia")
    if path:
        print("Path found:", " -> ".join(path))
    else:
        print("No path found.")

