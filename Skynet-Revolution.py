from sys import stderr
from collections import deque, defaultdict

class Vertex:
    def __init__(self, id: int):
            self.gateway = False
            self.id = id

    def print(self):
        print(f"Id: {self.id}, gateway: {self.gateway}", file=stderr, flush=True)

    def setGateway(self):
            self.gateway = True

class Graph:
    def __init__(self, n):
        self.graph = defaultdict(list)
        self.vertices = [Vertex(i) for i in range(n)]

    def addEdge(self, u: int, v: Vertex):
        self.graph[u].append(v)

    def removeEdge(self, u: int, v: Vertex):
        self.graph[u].remove(v)

    def gateways(self, u: int):
        gateways = []

        # Get all connected nodes that are gateways
        for vertex in self.graph[u]:
            if vertex.gateway:
                gateways.append(vertex)
        
        return gateways

    def BFS(self, s: int, t):
        # Initialize search
        Q = deque()
        V = set()

        # Prep search
        Q.append(s)
        V.add(s)

        while Q:
            # Get next node
            node = Q.popleft()

            # Get successors
            for next in self.graph[node]:
                if next not in V:
                    Q.append(next)
                    V.add(next)

    def findGateway(self, s: int):
        # Initialize search
        Q = deque()
        V = set()

        # Prep search
        Q.append(s)
        V.add(s)

        while Q:
            # Get next node
            node = Q.popleft()

            if self.vertices[node].gateway == True:
                return node

            # Get successors
            for next in self.graph[node]:
                if next.id not in V:
                    Q.append(next.id)
                    V.add(next.id)


def printError(target):
    print(target, file=stderr, flush=True)

def main():

    # n: the total number of nodes in the level, including the gateways
    # l: the number of links
    # e: the number of exit gateways
    n, l, e = [int(i) for i in input().split()]
    graph = Graph(n)

    for i in range(l):
        # n1: N1 and N2 defines a link between these nodes
        n1, n2 = [int(j) for j in input().split()]
        graph.addEdge(n1, graph.vertices[n2])
        graph.addEdge(n2, graph.vertices[n1])
        

    for i in range(e):
        ei = int(input())  # the index of a gateway node
        graph.vertices[ei].setGateway()

    # for vertex in graph.vertices:
    #     vertex.print()

    # printError("")

    # game loop
    while True:
        si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
        gateways = graph.gateways(si)
        if len(gateways) > 0:
            skynet = graph.vertices[si]
            node = gateways[0]
            print(f"{skynet.id} {node.id}")

            graph.removeEdge(skynet.id, node)
            graph.removeEdge(node.id, skynet)
        else:
            target = graph.findGateway(si)
            node = graph.graph[target][0]
            print(f"{target} {node.id}")

            graph.removeEdge(target, node)
            graph.removeEdge(node.id, graph.vertices[target])

if __name__ == "__main__":
    main()