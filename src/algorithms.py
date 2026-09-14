class Node:
    
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
      
        
    def reconstruct_path(goal_node):
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        path.reverse()
        return path       

        
start_node = Node((1, 1))
node_1 = Node((1, 2), parent=start_node, g=1)
node_2 = Node((2, 2), parent=node_1, g=2)
goal_node = Node((2, 3), parent=node_2, g=3)

path = Node.reconstruct_path(goal_node)

print(path)