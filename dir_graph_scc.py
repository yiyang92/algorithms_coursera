from __future__ import print_function

import collections
import time
import sys
import threading
import resource
import os

from kargerMinCut import Graph
# setting some finite recursion limit size
# setting recursion limit to infinity, can cause stack overflow! Doesnt work on Mac
# TODO: add check operation system statement
# resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


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
        self.dist = []

    def kosaraju(self):
        self._kosaraju_used = True
        rev_g = self.reversed_graph
        self.explored = [0] * (len(rev_g) + 1)
        print("Reversed")
        # 1-st pass
        for i in reversed(list(rev_g.keys())):
            if self.explored[i] != 1:
                self.s = i
                self.dfs_loop(i, rev_g)
        del self._reversed_graph
        del rev_g
        print("Second Pass")
        # 2-nd pass
        self.explored = [0] * (len(self.vertex) + 1)
        self.ld = {}
        for i in reversed(list(self.f_t.keys())):
            cur_vertex = self.f_t[i]
            if self.explored[cur_vertex] != 1:
                self.s = cur_vertex
                self.dfs_loop(cur_vertex, self.vertex, True)

    def dfs_loop(self, start_v, graph, second_pass=False):
        self.explored[start_v] = 1
        self.ld[start_v] = self.s
        for vtx in graph[start_v]:
            if self.explored[vtx] != 1:
                self.dfs_loop(vtx, graph, second_pass)
        if not second_pass:
            self.t += 1
            self.f_t[self.t] = start_v

    def dfs(self, start_v, graph):
        # stack - LIFO
        self.explored = [0] * (len(self.vertex) + 1)
        s = collections.deque()
        s.append(start_v)
        while s.count >= 1:
            v = s.pop()
            if self.explored[v] != 1:
                self.explored[v] = 1
                for vtx in graph[v]:
                    s.append(vtx)

    # used bfs to for computing shortest paths
    def bfs_dist(self, start_v):
        queue = collections.deque()
        if start_v in self.vertex:
            queue.append(start_v)
        else:
            print("Graph doesn`t contain selected starting vertex")
            exit()
        self.dist = [0] * (len(self.vertex) + 1)
        self.explored = [0] * (len(self.vertex) + 1)
        self.explored[start_v] = 1
        # queue - FIFO
        while len(queue) != 0:
            u = queue.popleft()
            print(u)
            for edge in self.vertex[u]:
                if self.explored[edge] == 0:
                    self.explored[edge] = 1
                    self.dist[edge] = self.dist[u] + 1
                    queue.append(edge)

    @property
    def reversed_graph(self):
        self._reversed_graph = {}
        for i in list(self.vertex.keys()):
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
        # you ned to run kosaraju algorithm first
        if not self._kosaraju_used:
            print("using kosaraju")
            self.kosaraju()
        ffc_num = [0] * (len(self.vertex)+1)
        for i in list(self.ld.keys()):
            ffc_num[self.ld[i]] += 1
        ffc_num = sorted(ffc_num)
        ffc_num.reverse()
        return ffc_num[:5]

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
    print("Number of fully connected componets is: ", graph.scc())
    graph.bfs_dist(1)
    print(graph.dist)

    sys.setrecursionlimit(2 ** 16)
    test_cases_path  = "./data/testCases/course2/assignment1SCC"
    graph3 = DirectedGraph()
    graph3.readGraphFromFile(os.path.join(test_cases_path, 'input_mostlyCycles_61_160000.txt'))
    graph3.kosaraju()
    print("Number of fully connected componets is: ", graph3.scc())
    # graph2 = DirectedGraph()
    # graph2.readGraphFromFile('./data/SCC.txt')
    # s_t = time.time()
    # graph2.kosaraju()
    # print("Number of fully connected componets is: ", graph2.scc())
    # print("Execution time: %.3f seconds" % (time.time() - s_t))

