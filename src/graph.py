# -*- encoding: utf-8 -*-
#
# comment
#
# 19-11-29 leo : Init

import numpy as np
import matplotlib.pyplot as plt

x = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]

game_qos = [0.993452685, 0.994021381, 0.99405142, 0.993587971, 0.993688188,
            0.993677027, 0.993188402, 0.993089349, 0.993103756, 0.993653245]
random_qos = [0.943938619, 0.924355272, 0.916988741, 0.911815736, 0.903594114,
              0.90311465, 0.900694066, 0.90100587, 0.90075647, 0.899133713]
greedy_qos = [0.987193181, 0.988549308, 0.983165108, 0.98888287, 0.992165796,
              0.989374438, 0.993088525, 0.992934507, 0.99381163, 0.995058395]
usage_qos = [0.912429668, 0.903227441, 0.898739708, 0.895798235, 0.892920318,
             0.892643271, 0.89125821, 0.888978077, 0.890417674, 0.888716211]

fig, ax = plt.subplots()
plt.xlabel('Number of MEC servers')
plt.ylabel('Average delay guarantee percentage (%)')
plt.plot(x, [i * 100 for i in game_qos], 'tomato', label='GOTA', marker='*')
plt.plot(x, [i * 100 for i in random_qos], 'orange', label='Random', marker='o', ls='--')
plt.plot(x, [i * 100 for i in greedy_qos], 'c', label='Delay optimal', marker='+', ls='-.')
plt.plot(x, [i * 100 for i in usage_qos], 'limegreen', label='RUF', marker='v', ls=':')
plt.ylim(85, 100)
plt.legend()
fig.savefig('qos.svg', dpi=600, format='svg')

game_usage = [0.483147936, 0.485792395, 0.488145251, 0.488222338, 0.490378926,
              0.490795257, 0.490931541, 0.490836516, 0.491907988, 0.491806512]
random_usage = [0.477228621, 0.493695954, .497223277, 0.501334347, 0.505955592,
                0.507616401, 0.507783733, 0.507928866, 0.508821806, 0.509417115]
greedy_usage = [0.173918294, 0.174917004, 0.175458807, 0.17632694, 0.176721459,
                0.177030212, 0.176927761, 0.177688656, 0.177632559, 0.177403082]
usage_usage = [0.503736578, 0.50632461, 0.507952367, 0.508915537, 0.511103971,
               0.51150056, 0.511857969, 0.5121699, 0.512877368, 0.512885405]

fig, ax = plt.subplots()
plt.xlabel('Number of MEC servers')
plt.ylabel('Average resource utilization rate of system (%)')
plt.plot(x, [i * 100 for i in game_usage], 'tomato', label='GOTA', marker='*')
plt.plot(x, [i * 100 for i in random_usage], 'orange', label='Random', marker='o', ls='--')
plt.plot(x, [i * 100 for i in greedy_usage], 'c', label='Delay optimal', marker='+', ls='-.')
plt.plot(x, [i * 100 for i in usage_usage], 'limegreen', label='RUF', marker='v', ls=':')
plt.ylim(10, 55)
plt.legend(loc='center right')
fig.savefig('utilization.svg', dpi=600, format='svg')

game_distribution = [{'local': 999, 'others': 4658, 'central_cloud': 4118},
                     {'local': 1090, 'others': 10261, 'central_cloud': 8386},
                     {'local': 1436, 'others': 15624, 'central_cloud': 12695},
                     {'local': 1593, 'others': 21131, 'central_cloud': 17045},
                     {'local': 1319, 'others': 27142, 'central_cloud': 21287},
                     {'local': 1434, 'others': 32725, 'central_cloud': 25621},
                     {'local': 1473, 'others': 38391, 'central_cloud': 29869},
                     {'local': 1695, 'others': 43864, 'central_cloud': 34173},
                     {'local': 1737, 'others': 49531, 'central_cloud': 38490},
                     {'local': 1757, 'others': 55228, 'central_cloud': 42746}]
random_distribution = [{'local': 1189, 'others': 4333, 'central_cloud': 4253},
                       {'local': 1386, 'others': 9660, 'central_cloud': 8691},
                       {'local': 1824, 'others': 14782, 'central_cloud': 13149},
                       {'local': 1820, 'others': 20305, 'central_cloud': 17644},
                       {'local': 1449, 'others': 26216, 'central_cloud': 22083},
                       {'local': 1634, 'others': 31555, 'central_cloud': 26593},
                       {'local': 1630, 'others': 37071, 'central_cloud': 31033},
                       {'local': 1900, 'others': 42322, 'central_cloud': 35510},
                       {'local': 1793, 'others': 47993, 'central_cloud': 39973},
                       {'local': 1784, 'others': 53539, 'central_cloud': 44413}]
greedy_distribution = [{'local': 1735, 'others': 3401, 'central_cloud': 4639},
                       {'local': 2581, 'others': 7746, 'central_cloud': 9410},
                       {'local': 3574, 'others': 11947, 'central_cloud': 14234},
                       {'local': 4256, 'others': 16450, 'central_cloud': 19063},
                       {'local': 4696, 'others': 21208, 'central_cloud': 23844},
                       {'local': 5409, 'others': 25677, 'central_cloud': 28696},
                       {'local': 5902, 'others': 30376, 'central_cloud': 33456},
                       {'local': 6958, 'others': 34526, 'central_cloud': 38248},
                       {'local': 7551, 'others': 39176, 'central_cloud': 43032},
                       {'local': 7997, 'others': 43858, 'central_cloud': 47881}]
usage_distribution = [{'local': 1192, 'others': 4357, 'central_cloud': 4226},
                      {'local': 1336, 'others': 9766, 'central_cloud': 8635},
                      {'local': 1711, 'others': 14927, 'central_cloud': 13117},
                      {'local': 1786, 'others': 20409, 'central_cloud': 17574},
                      {'local': 1500, 'others': 26243, 'central_cloud': 22005},
                      {'local': 1758, 'others': 31508, 'central_cloud': 26516},
                      {'local': 1647, 'others': 37155, 'central_cloud': 30932},
                      {'local': 1875, 'others': 42490, 'central_cloud': 35367},
                      {'local': 1908, 'others': 48049, 'central_cloud': 39802},
                      {'local': 1819, 'others': 53647, 'central_cloud': 44270}]

# game_sum = [d['local'] + d['others'] + d['central_cloud'] for d in game_distribution]
# random_sum = [d['local'] + d['others'] + d['central_cloud'] for d in random_distribution]
# greedy_sum = [d['local'] + d['others'] + d['central_cloud'] for d in greedy_distribution]
# usage_sum = [d['local'] + d['others'] + d['central_cloud'] for d in usage_distribution]

# game_local = [d['local'] / float(s) for (d, s) in zip(game_distribution, game_sum)]
# game_others = [d['others'] / float(s) for (d, s) in zip(game_distribution, game_sum)]
# game_cloud = [d['central_cloud'] / float(s) for (d, s) in zip(game_distribution, game_sum)]
# random_local = [d['local'] / float(s) for (d, s) in zip(random_distribution, random_sum)]
# random_others = [d['others'] / float(s) for (d, s) in zip(random_distribution, random_sum)]
# random_cloud = [d['central_cloud'] / float(s) for (d, s) in zip(random_distribution, random_sum)]
# greedy_local = [d['local'] / float(s) for (d, s) in zip(greedy_distribution, greedy_sum)]
# greedy_others = [d['others'] / float(s) for (d, s) in zip(greedy_distribution, greedy_sum)]
# greedy_cloud = [d['central_cloud'] / float(s) for (d, s) in zip(greedy_distribution, greedy_sum)]
# usage_local = [d['local'] / float(s) for (d, s) in zip(usage_distribution, usage_sum)]
# usage_others = [d['others'] / float(s) for (d, s) in zip(usage_distribution, usage_sum)]
# usage_cloud = [d['central_cloud'] / float(s) for (d, s) in zip(usage_distribution, usage_sum)]

# game_local = [d['local'] / (d['local'] + d['others'] + d['central_cloud']) for d in game_distribution]
# game_others = [d['others'] / (d['local'] + d['others'] + d['central_cloud']) for d in game_distribution]
# game_cloud = [d['central_cloud'] / (d['local'] + d['others'] + d['central_cloud']) for d in game_distribution]
# random_local = [d['local'] / (d['local'] + d['others'] + d['central_cloud']) for d in random_distribution]
# random_others = [d['others'] / (d['local'] + d['others'] + d['central_cloud']) for d in random_distribution]
# random_cloud = [d['central_cloud'] / (d['local'] + d['others'] + d['central_cloud']) for d in random_distribution]
# greedy_local = [d['local'] / (d['local'] + d['others'] + d['central_cloud']) for d in greedy_distribution]
# greedy_others = [d['others'] / (d['local'] + d['others'] + d['central_cloud']) for d in greedy_distribution]
# greedy_cloud = [d['central_cloud'] / (d['local'] + d['others'] + d['central_cloud']) for d in greedy_distribution]
# usage_local = [d['local'] / (d['local'] + d['others'] + d['central_cloud']) for d in usage_distribution]
# usage_others = [d['others'] / (d['local'] + d['others'] + d['central_cloud']) for d in usage_distribution]
# usage_cloud = [d['central_cloud'] / (d['local'] + d['others'] + d['central_cloud']) for d in usage_distribution]
#
# bar_x = list(range(len(x)))
# total_width, n = 0.8, 4
# width = total_width / n
# plt.xlabel('Number of MEC servers')
# plt.ylabel('Task allocation distribution')
# plt.bar(bar_x, game_local, width=width, label='GOTA-Local', fc='k', ec='r')
# plt.bar(bar_x, game_others, bottom=game_local, width=width, label='GOTA-Nearby', fc='grey', ec='r')
# plt.bar(bar_x, game_cloud, bottom=np.sum([game_local, game_others], axis=0), width=width, label='GOTA-RC', fc='silver', ec='r')
# for i in range(len(bar_x)):
#     bar_x[i] = bar_x[i] + width
# plt.bar(bar_x, random_local, width=width, label='Random-Local', fc='k', ec='y')
# plt.bar(bar_x, random_others, bottom=random_local, width=width, label='Random-Nearby', fc='grey', ec='y')
# plt.bar(bar_x, random_cloud, bottom=np.sum([random_local, random_others], axis=0), width=width, label='Random-RC', tick_label=x, fc='silver', ec='y')
# for i in range(len(bar_x)):
#     bar_x[i] = bar_x[i] + width
# plt.bar(bar_x, greedy_local, width=width, label='Delay optimal-Local', fc='k', ec='b')
# plt.bar(bar_x, greedy_others, bottom=greedy_local, width=width, label='Delay optimal-Nearby', fc='grey', ec='b')
# plt.bar(bar_x, greedy_cloud, bottom=np.sum([greedy_local, greedy_others], axis=0), width=width, label='Delay optimal-RC', fc='silver', ec='b')
# for i in range(len(bar_x)):
#     bar_x[i] = bar_x[i] + width
# plt.bar(bar_x, usage_local, width=width, label='RUF-Local', fc='k', ec='g')
# plt.bar(bar_x, usage_others, bottom=usage_local, width=width, label='RUF-Nearby', fc='grey', ec='g')
# plt.bar(bar_x, usage_cloud, bottom=np.sum([usage_local, usage_others], axis=0), width=width, label='RUF-RC', fc='silver', ec='g')
# plt.legend()

fig, ax = plt.subplots()
bar_name_list = ['Local server', 'Neighbor server', 'Remote cloud']
game_count = [game_distribution[4]['local'], game_distribution[4]['others'], game_distribution[4]['central_cloud']]
random_count = [random_distribution[4]['local'], random_distribution[4]['others'], random_distribution[4]['central_cloud']]
greedy_count = [greedy_distribution[4]['local'], greedy_distribution[4]['others'], greedy_distribution[4]['central_cloud']]
usage_count = [usage_distribution[4]['local'], usage_distribution[4]['others'], usage_distribution[4]['central_cloud']]
bar_x = list(range(len(bar_name_list)))
total_width, n = 0.8, 4
width = total_width / n
plt.xlabel('Task allocation strategy')
plt.ylabel('Task allocation statistics')
plt.bar(bar_x, game_count, fc='silver', width=width, label='GOTA', ec='k')
for i in range(len(bar_x)):
    bar_x[i] = bar_x[i] + width
plt.bar(bar_x, random_count, fc='grey', width=width, label='Random', ec='k')
for i in range(len(bar_x)):
    bar_x[i] = bar_x[i] + width
plt.bar(bar_x, greedy_count, fc='w', width=width, label='Delay optimal', tick_label=bar_name_list, ec='k')
for i in range(len(bar_x)):
    bar_x[i] = bar_x[i] + width
plt.bar(bar_x, usage_count, fc='k', width=width, label='RUF', ec='k')
plt.legend()
fig.savefig('strategy.svg', dpi=600, format='svg')

