# TODO: implement directed graph class, implement BFS and DFS(recursive and with stack)
# TODO: Your task is to code up the
# algorithm from the video lectures for
# computing strongly connected components (SCCs),
# and to run this algorithm on the given graph.

import collections
import time
import sys
import resource
import os

sys.setrecursionlimit(2 ** 30)

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
        print("Reversed")
        # some graphs start with 0, some (as in the input file) start with 1
        start_el = self.starting_value(rev_g)
        # 1-st pass
        for i in reversed(range(start_el, len(rev_g) + 1)):
            if i not in self.explored:
                self.s = i
                self.dfs_loop(i, rev_g)
        del self._reversed_graph
        del rev_g
        print("Second Pass")
        # 2-nd pass
        self.explored = []
        self.ld = {}
        for i in reversed(range(start_el, len(self.vertex) + 1)):
            cur_vertex = self.f_t[i]
            if cur_vertex not in self.explored:
                self.s = cur_vertex
                self.dfs_loop(cur_vertex, self.vertex, True)

    def dfs_loop(self, start_v, graph, second_pass=False):
        self.explored.append(start_v)
        self.ld[start_v] = self.s
        for vtx in graph[start_v]:
            if vtx not in self.explored:
                self.dfs_loop(vtx, graph, second_pass)
        if not second_pass:
            self.t += 1
            self.f_t[self.t] = start_v

    def reverse_graph(self):
        reverted = []
        s_v = self.starting_value(self.vertex)
        for i in range(s_v, len(self.vertex) + 1):
            temp = sorted(self.vertex[i])
            reverted.append(self.vertex[i])
            for j in range(len(temp)):
                if temp[j] not in reverted:
                    self.add_edge(temp[j], i)
                    del temp[j]

    @property
    def reversed_graph(self):
        self._reversed_graph = {}
        starting_el = self.starting_value(self.vertex)
        for i in range(starting_el, len(self.vertex) + 1):
            for vtx in self.vertex[i]:
                try:
                    self._reversed_graph[vtx].append(i)
                except KeyError:
                    self._reversed_graph[vtx] = [i]
            if i not in self._reversed_graph:
                self._reversed_graph[i] = []

        return self._reversed_graph

    def readGraphFromFile(self, file_name):
        with open(file_name) as rf:
            for line in rf:
                vtx1, vtx2 = [int(x) for x in line.strip().split(' ')]
                self.add_edge(vtx1, vtx2)
                if vtx2 not in self.vertex:
                    self.vertex[vtx2] = []


    def scc(self):
        # TODO: compute 5 SCC
        # you ned to run kosaraju algorithm first
        if not self._kosaraju_used:
            self.kosaraju()
        ffc = []
        for i in range(self.starting_value(self.vertex), len(self.ld) + 1):
            if self.ld[i] not in ffc:
                ffc.append(self.ld[i])
        return len(ffc)

    @staticmethod
    def starting_value(graph):
        try:
            _ = graph[0]
            start_el = 0
        except KeyError:
            start_el = 1
        return start_el


if __name__ == "__main__":
    graph = DirectedGraph()
    # graph from coursera algorithms ppt example
    for i in range(1, 7):
        graph.add_vertex(i)
    graph.add_edge(1, 4)
    graph.add_edge(4, 7)
    graph.add_edge(7, 1)
    graph.add_edge(9, 7)
    graph.add_edge(9, 3)
    graph.add_edge(3, 6)
    graph.add_edge(6, 9)
    graph.add_edge(8, 6)
    graph.add_edge(8, 5)
    graph.add_edge(5, 2)
    graph.add_edge(2, 8)
    graph.kosaraju()
    print("Time ", graph.f_t)
    print("Number of fully connected componets is: ", graph.ffc())

    test_cases_path  = "./data/testCases/course2/assignment1SCC"
    graph3 = DirectedGraph()
    graph3.readGraphFromFile(os.path.join(test_cases_path, 'input_mostlyCycles_38_3200.txt'))
    graph3.kosaraju()
    print("Number of fully connected componets is: ", graph3.ffc())
    # graph2 = DirectedGraph()
    # graph2.readGraphFromFile('./data/SCC.txt')
    # s_t = time.time()
    # graph2.kosaraju()
    # print("Number of fully connected componets is: ", graph2.ffc())
    # print("Execution time: %.3f seconds" % (time.time() - s_t))

