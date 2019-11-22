# -*- encoding: utf-8 -*-
#
# comment
#
# 19-11-19 leo : Init

import copy
import numpy as np
from utils import get_normal_random, get_random_memory, get_random_disk


class Task:
    def __init__(self, request_node):
        self.request_node = request_node
        self.DI = get_normal_random(mu=1000, sigma=256)
        self.DO = get_normal_random(mu=4000, sigma=512)
        self.ri = dict()
        self.ri['cpu'] = int(get_normal_random(mu=100, sigma=16.667))
        self.ri['memory'] = get_random_memory()
        self.ri['disk'] = get_random_disk()
        self.ri['bandwidth'] = int(get_normal_random(mu=100, sigma=16.667))
        self.nodes_delay = dict()
        for node in request_node.nodes():
            if node != request_node.name:
                if node == "central_cloud":
                    self.nodes_delay[node] = int(get_normal_random(mu=250, sigma=64))
                else:
                    self.nodes_delay[node] = int(get_normal_random(mu=100, sigma=16))
            else:
                self.nodes_delay[node] = int(get_normal_random(mu=50, sigma=8))
        self.CC = int(get_normal_random(mu=100, sigma=16))
        self.delta = 2000
        self.bi = 0

    def __repr__(self):
        return "Task<request_node=" + self.request_node.name + ", DI=" + \
                str(self.DI) + ', DO=' + str(self.DO) + ", ri=" + self.ri.__repr__() + \
                ", nodes_delay=" + self.nodes_delay.__repr__() + ", CC=" + \
                str(self.CC) + ', delta=' + str(self.delta) + '>'

    def set_bi(self, phi1, phi2):
        central_cloud = CentralCloud()
        para1 = phi1 / (phi1 + phi2)
        para2 = phi2 / (phi1 + phi2)
        dcci = self.DO / self.DI
        th = self.CC / central_cloud.Freq
        self.bi = para1 * dcci + para2 * th


class TaskStatus:
    START = 'start'
    INPUT = 'input'
    EXECUTE = "execute"
    OUTPUT = 'output'
    FINISHED = 'finished'


class ExecuteTask:
    def __init__(self, task, node):
        self.DI = task.DI
        self.DO = task.DO
        self.ri = task.ri
        self.node_delay = task.nodes_delay[node.name]
        self.CC = task.CC
        self.execute_node = node
        self.time_sum = 0
        self.rCC = copy.copy(self.CC)
        self.rDI = copy.copy(self.DI)
        self.rDO = copy.copy(self.DO)
        self.rDIdelay = copy.copy(self.node_delay)
        self.rDOdelay = copy.copy(self.node_delay)
        self.status = TaskStatus.START
        self.delta = task.delta


class Node:
    def __init__(self, name):
        self.name = name
        self.Ri = dict()
        self.Ri['cpu'] = 0
        self.Ri['memory'] = 0
        self.Ri['disk'] = 0
        self.Ri['bandwidth'] = 0
        self.Ci = dict()
        self.Ci['cpu'] = 1000
        self.Ci['memory'] = 32768
        self.Ci['disk'] = 8192
        self.Ci['bandwidth'] = 1000
        self.bandwidth = 112.5
        self.Freq = 4

    def nodes(self):
        node_list = list()
        node_list.append(self.name)
        graph = ConnectedGraph()
        for n in graph.links[self.name]:
            node_list.append(n)
        node_list.append('central_cloud')
        return node_list

    def __repr__(self):
        return "Node<name=" + self.name + ", Ri=" + self.Ri.__repr__() + ", Ci=" + \
                self.Ci.__repr__() + ", bandwidth=" + str(self.bandwidth) + \
                ", freq=" + str(self.Freq) + '>'


class ConnectedGraph:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, nodes=None, flag=False):
        if flag:
            self.links = dict()
            nodes_len = len(nodes)
            for node in nodes:
                self.links[node.name] = list()
            for node in nodes:
                # each node connect not more than nodes_len / 3 nodes
                connected_times = np.random.randint(1, nodes_len / 2)
                # check if node is not connected or over connected
                if len(self.links[node.name]) < connected_times:
                    while len(self.links[node.name]) < connected_times:
                        pick = np.random.randint(0, nodes_len)
                        if nodes[pick].name != node.name and not ConnectedGraph.check_node_in_link(node, nodes[pick].name):
                            self.links[node.name].append(nodes[pick].name)
                            self.links[nodes[pick].name].append(node.name)

    @classmethod
    def check_node_in_link(cls, node, check_name):
        flag = False
        for n in cls._instance.links[node.name]:
            if n.name == check_name:
                flag = True
        return flag

    def __repr__(self):
        return "ConnectedGraph<" + self.links.__repr__() + ">"


class CentralCloud:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, flag=False):
        if flag:
            self.name = 'central_cloud'
            self.Ri = dict()
            self.Ri['cpu'] = 0
            self.Ri['bandwidth'] = 0
            self.Ci = dict()
            self.Ci['cpu'] = 1000
            self.Ci['bandwidth'] = 1000
            self.bandwidth = 112.5
            self.Freq = 4

    def __repr__(self):
        return "CentralCloud<Ri=" + self.Ri.__repr__() + ", Ci=" + \
               self.Ci.__repr__() + ", bandwidth=" + str(self.bandwidth) + \
               ", Freq=" + str(self.Freq) + '>'



