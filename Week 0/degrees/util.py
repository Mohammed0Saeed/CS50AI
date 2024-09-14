class Node():
    def __init__(self):
        self.node = []

    def add_parent(self, node):
        self.node.append(node)

    def remove_parent(self):
        self.node = self.node[:-1]

    def optimize(self, node):
        """
        Returns an optimized solution or set of nodes with the shortest path
        """
        for i in range(len(node.show()) - 1):
            if node.show()[i][0] == node.show()[i+1][0]:
                shorter_path = node.show()[i+1]
                node.remove_parent()
                node.remove_parent()
                node.add_parent(shorter_path)

    def show(self):
        return self.node




class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def show(self):
        return self.frontier[-1]


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
