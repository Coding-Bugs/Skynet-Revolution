from sys import stderr
from collections import deque, defaultdict
from enum import IntEnum
from heapq import heappop, heappush

class NodeType(IntEnum):
    DEAD = 100
    ALIVE = 1
    DANGER = 2

class Vertex:
    def __init__(self, id: int):
            self.gateway = False
            self.id = id
            self.type = NodeType.DEAD

    def setType(self, type: NodeType):
        self.type = type


    def print(self):
        print(f"Id: {self.id}, gateway: {self.gateway}, Type: {self.type}", file=stderr, flush=True)

    def setGateway(self):
            self.gateway = True

class Graph:
    def __init__(self, n):
        self.graph = defaultdict(list)
        self.vertices = [Vertex(i) for i in range(n)]
    
    
    def print(self):
        for cnct in sorted(self.graph):
            self.vertices[cnct].print()

    def updateTypes(self, dead: bool):
        for node in self.vertices:
            # Don't waste time on dead nodes
            if not dead and node.type == NodeType.DEAD:
                continue
        
            gates = 0
            for cnct in self.graph[node.id]:
                if cnct.gateway == True:
                    gates += 1
            if gates > 1:
                node.setType(NodeType.DANGER)
            elif gates == 1:
                node.setType(NodeType.ALIVE)
            else: 
                node.setType(NodeType.DEAD)
    

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
    
    def greedy(self, s: int):
        # Initialize search
        Q = []
        V = set()

        # Prep search
        heappush(Q, (0, s))
        V.add(s)

        while Q:
            # Get next node
            tup = heappop(Q)
            prev = tup[0]
            node_idx = tup[1]

            if self.vertices[node_idx].type == NodeType.DANGER:
                return node_idx


            # Get successors
            for nxt in self.graph[node_idx]:
                val = int(nxt.type) + prev
                if nxt.id not in V:
                    heappush(Q, (val, nxt.id))
                    V.add(nxt.id)
        return None
    
        
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

    graph.updateTypes(True)

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
            graph.updateTypes(False)
        else:
            foo = graph.greedy(si)
            target = graph.gateways(foo)

            # If there is no double gates
            if target == []:
                target = graph.findGateway(si)
                node = graph.graph[target][0]
                print(f"{target} {node.id}")

                graph.removeEdge(target, node)
                graph.removeEdge(node.id, graph.vertices[target])
                graph.updateTypes(False)
                continue
            
            # kill a connection to the double gate
            node = target[0]
            print(f"{foo} {node.id}")

            graph.removeEdge(foo, node)
            graph.removeEdge(node.id, graph.vertices[foo])
            graph.updateTypes(False)

if __name__ == "__main__":
    main()