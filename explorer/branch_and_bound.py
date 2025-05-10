from dataStructures import Node
import heapq
from function_timer import timer

@timer
def branch_and_bound(start_title, goal_title):
    goal_node = Node(goal_title)
    goal_title = goal_node.title

    visited = set()
    best_path_length = float('inf')
    best_path = None

    queue = []
    heapq.heappush(queue, (0, [start_title]))

    while queue:
        current_cost, current_path = heapq.heappop(queue)
        current_title = current_path[-1]

        if current_title in visited:
            continue
        visited.add(current_title)

        if current_title == goal_title:
            if current_cost < best_path_length:
                best_path_length = current_cost
                best_path = current_path
            continue

        try:
            current_node = Node(current_title)
        except SyntaxError as e:
            print(e)
            continue

        if current_node.node_in_links(goal_title):
            new_path = current_path + [goal_title]
            new_cost = current_cost + 1
            if new_cost < best_path_length:
                best_path_length = new_cost
                best_path = new_path
            continue

        for link in current_node.get_links():
            if link not in visited:
                new_cost = current_cost + 1
                if new_cost < best_path_length:
                    heapq.heappush(queue, (new_cost, current_path + [link]))

    return best_path



if __name__ == "__main__":
    path = branch_and_bound("Amsterdam", "Asia")
    if path:
        print("Path found:", " -> ".join(path))
    else:
        print("No path found.")
