import heapq

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.neighbors = []

# Graph class
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, node1, node2, distance):
        # Undirected graph, so edges are added in both directions
        self.edges[(node1.id, node2.id)] = distance
        self.edges[(node2.id, node1.id)] = distance
        node1.neighbors.append(node2.id)
        node2.neighbors.append(node1.id)

    def calculate_shortest_path(self, start_node, end_node):
        # Dijkstra's algorithm for calculating the shortest path
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_node.id] = 0

        priority_queue = [(0, start_node.id)]

        while priority_queue:
            current_distance, current_node_id = heapq.heappop(priority_queue)

            if current_distance > distances[current_node_id]:
                continue

            for neighbor_id, edge_distance in self.get_neighbors(current_node_id):
                new_distance = distances[current_node_id] + edge_distance

                if new_distance < distances[neighbor_id]:
                    distances[neighbor_id] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor_id))

        return distances[end_node.id]

    def get_neighbors(self, node_id):
        # Helper function to get neighbors of a node
        return [(neighbor_id, self.edges[(node_id, neighbor_id)]) for neighbor_id in self.nodes[node_id].neighbors]

# Driver Code
if __name__ == "__main__":
    # Creating nodes
    branch1 = Node("Branch1")
    branch2 = Node("Branch2")
    service_point1 = Node("ServicePoint1")
    service_point2 = Node("ServicePoint2")

    # Creating graph
    graph = Graph()

    # Adding nodes to the graph
    graph.add_node(branch1)
    graph.add_node(branch2)
    graph.add_node(service_point1)
    graph.add_node(service_point2)

    # Adding edges with distances
    graph.add_edge(branch1, service_point1, 5)
    graph.add_edge(branch1, service_point2, 8)
    graph.add_edge(branch2, service_point1, 10)
    graph.add_edge(service_point1, service_point2, 3)

    # Calculating the shortest path between two nodes
    start_node = branch1
    end_node = service_point2

    shortest_distance = graph.calculate_shortest_path(start_node, end_node)

    if shortest_distance == float('inf'):
        print(f"There is no path from {start_node.id} to {end_node.id}.")
    else:
        print(f"Shortest Distance from {start_node.id} to {end_node.id}: {shortest_distance}")
