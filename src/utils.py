# -*- encoding: utf-8 -*-
#
# comment
#
# 19-11-19 leo : Init

import numpy as np


def get_normal_random(mu=0, sigma=1):
    return sigma * np.random.randn() + mu


def get_random_memory():
    random_exp = np.random.randint(7, 12, 6)
    memory_list = 2 ** random_exp
    return memory_list[np.random.randint(0, 6)]


def get_random_disk():
    random_exp = np.random.randint(2, 7, 6)
    disk_list = 2 ** random_exp
    return disk_list[np.random.randint(0, 6)]


def get_lix(task, node):
    tcom = task.CC / (task.ri['cpu'] * node.Freq / (task.ri['cpu'] + node.Ri['cpu']))
    ttrans = (task.DI + task.DO) * (node.Ri['bandwidth'] + task.ri['bandwidth']) / \
             (task.ri['bandwidth'] * node.bandwidth) + 2 * task.nodes_delay[node.name]
    tix = ttrans + tcom
    # print("time estimate: " + str(tix))
    if task.delta > tix:
        return task.delta / (task.delta - tix)
    else:
        return -1


def get_rho_ix(task, node):
    eix = 0
    for q in task.ri.keys():
        used = task.ri[q] + node.Ri[q]
        if used > node.Ci[q]:
            return -1
        eix += used / node.Ci[q]
    # print("node cost: " + str(eix))
    return eix


def check_available(task, node):
    for q in task.ri.keys():
        if task.ri[q] + node.Ri[q] > node.Ci[q]:
            return False
    return True


def get_load_percentage(nodes):
    n_sum = 0
    for node in nodes:
        q_sum = 0
        for q in node.Ri.keys():
            q_sum += node.Ri[q] / node.Ci[q]
        q_sum /= 4
        n_sum += q_sum
    return n_sum / len(nodes)


def get_balance_percentage(nodes):
    n_sum = 0
    for node in nodes:
        q_max = 0
        q_min = 20
        for q in node.Ri.keys():
            rate = node.Ri[q] / node.Ci[q]
            if rate > q_max:
                q_max = rate
            if rate < q_min:
                q_min = rate
        n_sum += abs(q_max - q_min)
    return n_sum / len(nodes)


def get_tix(task, node):
    tcom = task.CC / (task.ri['cpu'] * node.Freq / (task.ri['cpu'] + node.Ri['cpu']))
    ttrans = (task.DI + task.DO) * (node.Ri['bandwidth'] + task.ri['bandwidth'])  / \
             (task.ri['bandwidth'] * node.bandwidth) + 2 * task.nodes_delay[
                 node.name]
    tix = ttrans + tcom
    return tix
