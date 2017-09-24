# TODO: implement directed graph class, implement BFS and DFS(recursive and with stack)
# TODO: Your task is to code up the
# algorithm from the video lectures for
# computing strongly connected components (SCCs),
# and to run this algorithm on the given graph.

import collections
import time

from kargerMinCut import Graph


class DirectedGraph(Graph):
    def __init__(self):
        super(Graph).__init__()
        self.vertex = {}
        self._reversed_graph = {}
        # variables for kosaraju`s
        self.explored = []
        # f_t - 'finishing time', ld - 'leaders'
        self.f_t = {}
        self.ld = {}
        self.s = 0
        self.t = 0
        # check if kosaraju algorithm was used
        self._kosaraju_used = False

    def kosaraju(self):
        self._kosaraju_used = True
        rev_g = self.reversed_graph
        # some graphs start with 0, some (as in the input file) start with 1
        try:
            _ = rev_g[0]
            start_el = 0
        except KeyError:
            print("Graph must be starting from one")
            start_el = 1

        # 1-st pass
        for i in reversed(range(start_el, len(rev_g))):
            if i not in self.explored:
                self.s = i
                self.dfs_loop(i, rev_g)
        # 2-nd pass
        self.explored = []
        f_t = self.f_t
        for i in reversed(range(start_el, len(self.vertex))):
            if i not in self.explored:
                self.s = f_t[i]
                self.dfs_loop(self.f_t[i], self.vertex)

    def dfs_loop(self, start_v, graph):
        self.explored.append(start_v)
        self.ld[start_v] = self.s
        for vtx in graph[start_v]:
            if vtx not in self.explored:
                self.dfs_loop(vtx, graph)
        self.t += 1
        self.f_t[self.t] = start_v

    def reverse_graph(self):
        # TODO: cases - only one edge - easy; more edges-?
        reverted = []
        for i in range(len(self.vertex)):
            temp = sorted(self.vertex[i])
            reverted.append(self.vertex[i])
            for j in range(len(temp)):
                if temp[j] not in reverted:
                    self.add_edge(temp[j], i)
                    del temp[j]

    @property
    def reversed_graph(self):
        self._reversed_graph = {}
        for i in range(len(self.vertex)):
            for vtx in self.vertex[i]:
                try:
                    self._reversed_graph[vtx].append(i)
                except KeyError:
                    self._reversed_graph[vtx] = [i]
        self._reversed_graph[0] = []
        return self._reversed_graph

    def readGraphFromFile(self, file_name):
        with open(file_name) as rf:
            for line in rf:
                vtx1, vtx2 = line.strip().split(' ')
                try:
                    self._reversed_graph[vtx1].append(vtx2)
                except KeyError:
                    self._reversed_graph[vtx1] = [vtx2]

    def ffc(self):
        # you ned to run kosaraju algorithm first
        if not self._kosaraju_used:
            self.kosaraju()
        ffc = []
        for i in range(len(self.ld)):
            if self.ld[i] not in ffc:
                ffc.append(self.ld[i])
        print(ffc)
        return len(ffc)


if __name__ == "__main__":
    graph = DirectedGraph()
    # graph from coursera algorithms ppt example
    for i in range(7):
        graph.add_vertex(i)
    graph.add_edge(0, 6)
    graph.add_edge(6, 3)
    graph.add_edge(3, 0)
    graph.add_edge(6, 8)
    graph.add_edge(8, 5)
    graph.add_edge(5, 2)
    graph.add_edge(2, 8)
    graph.add_edge(5, 7)
    graph.add_edge(7, 1)
    graph.add_edge(1, 4)
    graph.add_edge(4, 7)
    print(graph)
    graph.kosaraju()
    print(graph.ld)
    print(graph.ffc())

    # graph2 = DirectedGraph()
    # graph2.readGraphFromFile('./data/SCC.txt')
    # s_t = time.time()
    # graph2.kosaraju()
    # print("Execution time: %.3f seconds" % (time.time() - s_t))
    #
