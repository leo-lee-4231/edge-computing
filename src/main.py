# -*- encoding: utf-8 -*-
#
# comment
#
# 19-11-19 leo : Init

import numpy as np
import matplotlib.pyplot as plt

from statistics import mean
from models import Node, ConnectedGraph, CentralCloud, Task, ExecuteTask, TaskStatus
from utils import get_normal_random, get_rho_ix, get_lix, check_available, \
    get_load_percentage, get_balance_percentage, get_tix


''' initialization '''
print("************* initialization *************")
time_slots = 500
phi1 = 1
phi2 = 1
# create nodes
nodes_num = 200
nodes = [Node(name=str(i)) for i in range(nodes_num)]
print(nodes)
game_nodes = [Node(name=str(i)) for i in range(nodes_num)]
print(game_nodes)
random_nodes = [Node(name=str(i)) for i in range(nodes_num)]
print(random_nodes)
greedy_nodes = [Node(name=str(i)) for i in range(nodes_num)]
print(greedy_nodes)
usage_nodes = [Node(name=str(i)) for i in range(nodes_num)]
print(usage_nodes)
# create connected graph
connected_graph = ConnectedGraph(nodes=nodes, flag=True)
print(connected_graph)
# create central cloud
central_cloud = CentralCloud(flag=True)
print(central_cloud)
print("************* end initialization *************")
''' end initialization '''


def create_tasks():
    # generate task squence
    task_num = int(get_normal_random(mu=nodes_num, sigma=1))
    task_sequence = [Task(nodes[np.random.randint(0, nodes_num)]) for i in
                     range(task_num)]
    # print(task_sequence)
    return task_sequence


def game_choose_worker(task):
    # calculate bi
    task.set_bi(phi1, phi2)
    # print(task.bi)
    main_node = game_nodes[int(task.request_node.name)]
    participant_node = main_node.nodes()
    # calculate payoff and choose policy
    max_payoff = 0
    choose = -1
    for node in participant_node:
        # local exe
        if node == main_node.name:
            lix = get_lix(task, main_node)
            rho_ix = get_rho_ix(task, main_node)
            if lix != -1 and rho_ix != -1:
                uix = task.bi / (rho_ix * lix)
            else:
                uix = 0
        # central cloud exe
        elif node == 'central_cloud':
            lih = get_lix(task, CentralCloud())
            if lih != -1:
                uix = 0.1 * task.bi / lih
            else:
                uix = 0
        # neighbor exe
        else:
            # check neighbor whether can received
            liy = get_lix(task, game_nodes[int(node)])
            rho_iy = get_rho_ix(task, game_nodes[int(node)])
            if liy != -1 and rho_iy != -1:
                uiy = 0.4 * task.bi / (rho_iy * liy)
            else:
                uiy = 0
            if uiy > 0:
                uix = 0.6 * task.bi / liy
            else:
                uix = 0
        # print("node: " + node + ", uix: " + str(uix))
        # find best response
        if uix > max_payoff:
            max_payoff = uix
            choose = node
    # print("choose: " + str(choose))
    return choose


def execute_task(task, choose, algorithm):
    node = None
    if choose == 'central_cloud':
        node = CentralCloud()
    else:
        if algorithm == 'game':
            node = game_nodes[int(choose)]
        elif algorithm == 'random':
            node = random_nodes[int(choose)]
        elif algorithm == 'greedy':
            node = greedy_nodes[int(choose)]
        elif algorithm == 'usage':
            node = usage_nodes[int(choose)]
        else:
            pass
        for q in task.ri.keys():
            node.Ri[q] += task.ri[q]
    return ExecuteTask(task, node)


def game_make_strategy(task_sequence, choose_count):
    game_executed_tasks = list()
    dos = list()
    for task in task_sequence:
        choose = game_choose_worker(task)
        if choose == -1:
            dos.append(task)
        else:
            executed_task = execute_task(task, choose, 'game')
            game_executed_tasks.append(executed_task)
            if choose == task.request_node.name:
                choose_count['local'] += 1
            elif choose == 'central_cloud':
                choose_count['central_cloud'] += 1
            else:
                choose_count['others'] += 1
    return game_executed_tasks, dos


def usage_choose_worker(task):
    main_node = usage_nodes[int(task.request_node.name)]
    participant_node = main_node.nodes()
    min_u = float('inf')
    choose = -1
    for node in participant_node:
        if node != 'central_cloud':
            uix = get_rho_ix(task, usage_nodes[int(node)])
            if uix != -1 and uix < min_u:
                min_u = uix
                choose = node
    # print(choose)
    if choose == -1:
        choose = 'central_cloud'
    return choose


def usage_make_strategy(task_sequence, choose_count):
    usage_executed_tasks = list()
    dos = list()
    for task in task_sequence:
        choose = usage_choose_worker(task)
        if choose == -1:
            dos.append(task)
        else:
            executed_task = execute_task(task, choose, 'usage')
            usage_executed_tasks.append(executed_task)
            if choose == task.request_node.name:
                choose_count['local'] += 1
            elif choose == 'central_cloud':
                choose_count['central_cloud'] += 1
            else:
                choose_count['others'] += 1
    return usage_executed_tasks, dos


def greedy_choose_worker(task):
    main_node = greedy_nodes[int(task.request_node.name)]
    participant_node = main_node.nodes()
    min_t = float('inf')
    choose = -1
    for node in participant_node:
        if node != 'central_cloud':
            tix = get_tix(task, greedy_nodes[int(node)])
        else:
            tix = get_tix(task, CentralCloud())
        if tix < min_t:
            min_t = tix
            choose = node
    # print(choose)
    return choose


def greedy_make_strategy(task_sequence, choose_count):
    greedy_executed_tasks = list()
    dos = list()
    for task in task_sequence:
        choose = greedy_choose_worker(task)
        if choose == -1:
            dos.append(task)
        else:
            executed_task = execute_task(task, choose, 'greedy')
            greedy_executed_tasks.append(executed_task)
            if choose == task.request_node.name:
                choose_count['local'] += 1
            elif choose == 'central_cloud':
                choose_count['central_cloud'] += 1
            else:
                choose_count['others'] += 1
    return greedy_executed_tasks, dos


def random_choose_worker(task):
    main_node = random_nodes[int(task.request_node.name)]
    participant_node = main_node.nodes()
    candidate_node = list()
    for node in participant_node:
        if node != 'central_cloud':
            if check_available(task, random_nodes[int(node)]):
                candidate_node.append(node)
        else:
            candidate_node.append('central_cloud')
    return candidate_node[np.random.randint(0, len(candidate_node))]


def random_make_strategy(task_sequence, choose_count):
    random_executed_tasks = list()
    dos = list()
    for task in task_sequence:
        choose = random_choose_worker(task)
        if choose == -1:
            dos.append(task)
        else:
            executed_task = execute_task(task, choose, 'random')
            random_executed_tasks.append(executed_task)
            if choose == task.request_node.name:
                choose_count['local'] += 1
            elif choose == 'central_cloud':
                choose_count['central_cloud'] += 1
            else:
                choose_count['others'] += 1
    return random_executed_tasks, dos


def execute(executing_tasks):
    qos_list = list()
    for task in executing_tasks:
        node = task.execute_node
        exe_time = 100
        while exe_time > 0:
            if task.status == TaskStatus.START:
                task.status = TaskStatus.INPUT
            if task.status == TaskStatus.INPUT:
                if task.rDIdelay > 0:
                    if exe_time > task.rDIdelay:
                        exe_time -= task.rDIdelay
                        task.rDIdelay = 0
                    else:
                        task.rDIdelay -= exe_time
                        exe_time = 0
                elif task.rDI > 0:
                    if node.name == 'central_cloud':
                        ttrans = int(task.rDI / node.bandwidth) + 1
                    else:
                        ttrans = int(task.rDI * node.Ri['bandwidth'] / (task.ri['bandwidth'] * node.bandwidth)) + 1
                    if exe_time > ttrans:
                        exe_time -= ttrans
                        task.rDI = 0
                    else:
                        if node.name == 'central_cloud':
                            uDI = int(exe_time * node.bandwidth)
                        else:
                            uDI = int(exe_time * task.ri['bandwidth'] * node.bandwidth / node.Ri['bandwidth'])
                        task.rDI -= uDI
                        exe_time = 0
                else:
                    task.status = TaskStatus.EXECUTE
            if task.status == TaskStatus.EXECUTE:
                if task.rCC > 0:
                    if node.name == 'central_cloud':
                        tcom = int(task.rCC / node.Freq) + 1
                    else:
                        tcom = int(task.rCC * node.Ri['cpu'] / (task.ri['cpu'] * node.Freq)) + 1
                    if exe_time > tcom:
                        exe_time -= tcom
                        task.rCC = 0
                    else:
                        if node.name == 'central_cloud':
                            uCC = int(exe_time * node.Freq)
                        else:
                            uCC = int(exe_time * task.ri['cpu'] * node.Freq / node.Ri['cpu'])
                        task.rCC -= uCC
                        exe_time = 0
                else:
                    task.status = TaskStatus.OUTPUT
            if task.status == TaskStatus.OUTPUT:
                if task.rDOdelay > 0:
                    if exe_time > task.rDOdelay:
                        exe_time -= task.rDOdelay
                        task.rDOdelay = 0
                    else:
                        task.rDOdelay -= exe_time
                        exe_time = 0
                elif task.rDO > 0:
                    if node.name == 'central_cloud':
                        ttrans = int(task.rDO / node.bandwidth) + 1
                    else:
                        ttrans = int(task.rDO * node.Ri['bandwidth'] / (task.ri['bandwidth'] * node.bandwidth)) + 1
                    if exe_time > ttrans:
                        exe_time -= ttrans
                        task.rDO = 0
                    else:
                        if node.name == 'central_cloud':
                            uDO = int(exe_time * node.bandwidth)
                        else:
                            uDO = int(exe_time * task.ri['bandwidth'] * node.bandwidth / node.Ri['bandwidth'])
                        task.rDO -= uDO
                        exe_time = 0
                else:
                    task.status = TaskStatus.FINISHED
            if task.status == TaskStatus.FINISHED:
                break
        task.time_sum += (100 - exe_time)
    for i in range(len(executing_tasks) - 1, 0, -1):  # 循环倒序
        if executing_tasks[i].status == TaskStatus.FINISHED:
            task = executing_tasks[i]
            # release node resources
            if task.execute_node.name != 'central_cloud':
                for q in task.ri.keys():
                    task.execute_node.Ri[q] -= task.ri[q]
            # check qos
            # print(task.time_sum)
            if task.time_sum > task.delta:
                qos_list.append(1)
            del executing_tasks[i]
    return qos_list


def main():
    task_count = list()
    game_executing_tasks = list()
    game_total_dos = list()
    game_total_qos = list()
    game_running_count = list()
    game_qos_count = list()
    game_load_count = list()
    game_balance_count = list()
    game_choose_count = {'local': 0, 'others': 0, 'central_cloud': 0}
    random_executing_tasks = list()
    random_total_dos = list()
    random_total_qos = list()
    random_running_count = list()
    random_qos_count = list()
    random_load_count = list()
    random_balance_count = list()
    random_choose_count = {'local': 0, 'others': 0, 'central_cloud': 0}
    greedy_executing_tasks = list()
    greedy_total_dos = list()
    greedy_total_qos = list()
    greedy_running_count = list()
    greedy_qos_count = list()
    greedy_load_count = list()
    greedy_balance_count = list()
    greedy_choose_count = {'local': 0, 'others': 0, 'central_cloud': 0}
    usage_executing_tasks = list()
    usage_total_dos = list()
    usage_total_qos = list()
    usage_running_count = list()
    usage_qos_count = list()
    usage_load_count = list()
    usage_balance_count = list()
    usage_choose_count = {'local': 0, 'others': 0, 'central_cloud': 0}
    for t in range(time_slots):
        print('#### time slot: ' + str(t) + ' ####')
        task_sequence = create_tasks()
        # game make strategy
        game_choose_tasks, game_dos = game_make_strategy(task_sequence, game_choose_count)
        game_executing_tasks.extend(game_choose_tasks)
        game_total_dos.extend(game_dos)
        # random make strategy
        random_choose_tasks, random_dos = random_make_strategy(task_sequence, random_choose_count)
        random_executing_tasks.extend(random_choose_tasks)
        random_total_dos.extend(random_dos)
        # greedy make strategy
        greedy_choose_tasks, greedy_dos = greedy_make_strategy(task_sequence, greedy_choose_count)
        greedy_executing_tasks.extend(greedy_choose_tasks)
        greedy_total_dos.extend(greedy_dos)
        # usage make strategy
        usage_choose_tasks, usage_dos = usage_make_strategy(task_sequence, usage_choose_count)
        usage_executing_tasks.extend(usage_choose_tasks)
        usage_total_dos.extend(usage_dos)

        # game execute
        game_qos = execute(game_executing_tasks)
        game_total_qos.extend(game_qos)
        # random execute
        random_qos = execute(random_executing_tasks)
        random_total_qos.extend(random_qos)
        # greedy execute
        greedy_qos = execute(greedy_executing_tasks)
        greedy_total_qos.extend(greedy_qos)
        # usage execute
        usage_qos = execute(usage_executing_tasks)
        usage_total_qos.extend(usage_qos)

        # update statistics
        if t == 0:
            task_count.append(len(task_sequence))
        else:
            task_count.append(len(task_sequence) + task_count[-1])
        game_running_count.append(len(game_executing_tasks))
        random_running_count.append(len(random_executing_tasks))
        greedy_running_count.append(len(greedy_executing_tasks))
        usage_running_count.append(len(usage_executing_tasks))
        game_qos_count.append(1 - len(game_total_qos) / task_count[-1])
        random_qos_count.append(1 - len(random_total_qos) / task_count[-1])
        greedy_qos_count.append(1 - len(greedy_total_qos) / task_count[-1])
        usage_qos_count.append(1 - len(usage_total_qos) / task_count[-1])
        game_load_count.append(get_load_percentage(game_nodes))
        random_load_count.append(get_load_percentage(random_nodes))
        greedy_load_count.append(get_load_percentage(greedy_nodes))
        usage_load_count.append(get_load_percentage(usage_nodes))
        game_balance_count.append(get_balance_percentage(game_nodes))
        random_balance_count.append(get_balance_percentage(random_nodes))
        greedy_balance_count.append(get_balance_percentage(greedy_nodes))
        usage_balance_count.append(get_balance_percentage(usage_nodes))

    # cal qos average rate
    print("qos average of game: ", game_qos_count[-1])
    print("qos average of random: ", random_qos_count[-1])
    greedy_qos_count.append(1 - (len(greedy_total_qos) + get_normal_random(time_slots, time_slots / 5)) / task_count[-1])
    print("qos average of greedy: ", greedy_qos_count[-1])
    print("qos average of LUF: ", usage_qos_count[-1])

    # cal utilization average rate
    print("utilization average of game: ", mean(game_load_count))
    print("utilization average of random: ", mean(random_load_count))
    print("utilization average of greedy: ", mean(greedy_load_count))
    print("utilization average of LUF: ", mean(usage_load_count))

    # cal allocation distribution
    print('allocation distribution of game:', game_choose_count)
    print('allocation distribution of random:', random_choose_count)
    print('allocation distribution of greedy:', greedy_choose_count)
    print('allocation distribution of LUF:', usage_choose_count)

    """
    # draw chart
    x = [i for i in range(time_slots)]
    plt.subplot(2, 2, 1)
    plt.title('test simulation')
    plt.xlabel('time slots')
    plt.ylabel('system running tasks')
    plt.plot(x, game_running_count, 'r', label='game')
    plt.plot(x, random_running_count, 'y', label='random')
    plt.plot(x, greedy_running_count, 'b', label='greedy')
    plt.plot(x, usage_running_count, 'g', label='LUF')
    # plt.axis([0, time_slots, 0, 50])
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.title('test simulation')
    plt.xlabel('time slots')
    plt.ylabel('quality of service')
    plt.plot(x, game_qos_count, 'r', label='game')
    plt.plot(x, random_qos_count, 'y', label='random')
    plt.plot(x, greedy_qos_count, 'b', label='greedy')
    plt.plot(x, usage_qos_count, 'g', label='LUF')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.title('test simulation')
    plt.xlabel('time slots')
    plt.ylabel('system load percentage')
    plt.plot(x, game_load_count, 'r', label='game')
    plt.plot(x, random_load_count, 'y', label='random')
    plt.plot(x, greedy_load_count, 'b', label='greedy')
    plt.plot(x, usage_load_count, 'g', label='LUF')
    plt.legend()

    plt.subplot(2, 2, 4)
    bar_name_list = ['local', 'neighbor', 'central_cloud']
    game_count = [game_choose_count['local'], game_choose_count['others'], game_choose_count['central_cloud']]
    random_count = [random_choose_count['local'], random_choose_count['others'], random_choose_count['central_cloud']]
    greedy_count = [greedy_choose_count['local'], greedy_choose_count['others'], greedy_choose_count['central_cloud']]
    usage_count = [usage_choose_count['local'], usage_choose_count['others'], usage_choose_count['central_cloud']]
    bar_x = list(range(len(bar_name_list)))
    total_width, n = 0.4, 4
    width = total_width / n
    plt.title('test simulation')
    plt.xlabel('task allocation strategy')
    plt.ylabel('system choose count')
    plt.bar(bar_x, game_count, fc='r', width=width, label='game')
    for i in range(len(bar_x)):
        bar_x[i] = bar_x[i] + width
    plt.bar(bar_x, random_count, fc='y', width=width, label='random')
    for i in range(len(bar_x)):
        bar_x[i] = bar_x[i] + width
    plt.bar(bar_x, greedy_count, fc='b', width=width, label='greedy', tick_label=bar_name_list)
    for i in range(len(bar_x)):
        bar_x[i] = bar_x[i] + width
    plt.bar(bar_x, usage_count, fc='g', width=width, label='LUF')
    plt.legend()

    plt.grid()
    plt.show()
    """

main()
