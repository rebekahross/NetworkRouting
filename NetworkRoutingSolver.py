#!/usr/bin/python3
from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        if self.dist[self.dest] == math.inf:
            return {'cost':math.inf, 'path':[]}
        total_length = self.dist[self.dest]
        edges = []
        cur_node = self.dest
        prev_node = self.prev[self.dest]
        for i in range(len(self.prev)):
            edges.append((prev_node, cur_node))
            cur_node = prev_node
            prev_node = self.prev[prev_node]
            if prev_node == None:
                break
        edges.reverse()
        path_edges = []
        for edge in edges:
            for i in range(3):
                if self.network.nodes[edge[0]].neighbors[i].dest == self.network.nodes[edge[1]]:
                    path_edges.append((self.network.nodes[edge[0]].loc, self.network.nodes[edge[1]].loc, '{:.0f}'.format(self.network.nodes[edge[0]].neighbors[i].length)))
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap == True:
            self.dist, self.prev = self.dijkstrasHeap(self.network, srcIndex)
        elif use_heap == False:
            self.dist, self.prev = self.dijkstrasArray(self.network, srcIndex)
        t2 = time.time()
        return (t2-t1)


    def dijkstrasHeap(self, graph, s):
        G = graph.getNodes()
        dist = [math.inf for i in range(len(G))]
        prev = [None for i in range(len(G))]
        dist[s] = 0
        pq = PriorityQueueBinaryHeap()
        pq.make_queue(len(G), s)
        while pq.queue:
            u = pq.delete_min()
            for edge in G[u].neighbors:
                if dist[edge.dest.node_id] > dist[u] + edge.length:
                    dist[edge.dest.node_id] = dist[u] + edge.length
                    prev[edge.dest.node_id] = u
                    pq.decrease_key(dist[edge.dest.node_id], edge.dest.node_id)
        return dist, prev

    def dijkstrasArray( self, graph, s):
        G = graph.getNodes()
        dist = [math.inf for i in range(len(G))]
        prev = [None for i in  range(len(G))]
        pq = PriorityQueueUnsortedArray()
        dist[s] = 0
        pq.make_queue(len(G), s)
        while len(pq.queue) > 0:
            u = pq.delete_min()
            for edge in G[u].neighbors:
                if dist[edge.dest.node_id] > dist[u] + edge.length:
                    dist[edge.dest.node_id] = dist[u] + edge.length
                    prev[edge.dest.node_id] = u
                    pq.decrease_key(dist[edge.dest.node_id], edge.dest.node_id)
        return dist, prev

class PriorityQueueUnsortedArray:
    def __init__(self):
        self.queue = {}

    def make_queue(self, length, s):
        for i in range(length):
            self.insert(math.inf, i)
        self.queue[s] = 0

    def insert(self, dist, node):
        self.queue[node] = dist

    def delete_min(self):
        u = min(self.queue, key=self.queue.get)
        self.queue.pop(u)
        return u

    def decrease_key(self, dist, node):
        self.queue[node] = dist


class PriorityQueueBinaryHeap:
    def __init__(self):
        self.queue = []
        self.pointers = []

    def make_queue(self, length, s):
        for i in range(length):
            self.pointers.append(i)
        self.queue.append((0,s))
        self.pointers[s] = 0

    def insert(self, dist, node):
        self.queue.append([dist, node])
        self.pointers[node] = len(self.queue) - 1
        # self.move_up(len(self.queue) - 1)

    def delete_min(self):
        if len(self.queue) == 1:
            return self.queue.pop()[1]
        u = self.queue[0][1]
        self.pointers[self.queue[len(self.queue) - 1][1]] = 0
        self.pointers[self.queue[0][1]] = -1
        self.queue[0] = self.queue[len(self.queue) - 1]
        self.queue.pop()
        self.move_down(0)
        return u

    def decrease_key(self, dist, node):
        self.queue.append((dist, node))
        self.pointers[node] = len(self.queue) - 1
        self.move_up(self.pointers[node])

    def move_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.queue[index][0] < self.queue[parent_index][0]:
                temp = self.pointers[self.queue[index][1]]
                self.pointers[self.queue[index][1]] = self.pointers[self.queue[parent_index][1]]
                self.pointers[self.queue[parent_index][1]] = temp

                temp = self.queue[index]
                self.queue[index] = self.queue[parent_index]
                self.queue[parent_index] = temp
                index = parent_index
            else:
                break
        return


    def move_down(self, index):
        while True:
            left_child_index = (2 * index) + 1
            right_child_index = (2 * index) + 2
            smallest = index
            if left_child_index < len(self.queue) and self.queue[left_child_index][0] < self.queue[smallest][0]:
                smallest = left_child_index
            if right_child_index < len(self.queue) and self.queue[right_child_index][0] < self.queue[smallest][0]:
                smallest = right_child_index
            if smallest == index:
                break
            temp = self.pointers[self.queue[index][1]]
            self.pointers[self.queue[index][1]] = self.pointers[self.queue[smallest][1]]
            self.pointers[self.queue[smallest][1]] = temp

            temp = self.queue[index]
            self.queue[index] = self.queue[smallest]
            self.queue[smallest] = temp

            index = smallest