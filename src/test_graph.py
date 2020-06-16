# -*- encoding: utf-8 -*-
#
# comment
#
# 20-4-15 leo : Init

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

bar_name_list = ['(22,2)', '(23,2)', '(24,2)', '(25,2)', '(26,2)', '(27,2)', '(28,2)', '(29,2)']
local_time = [0.437, 0.875, 1.779, 3.664, 7.546, 15.616, 32.389, 66.882]
offload_time = [0.331, 0.677, 1.266, 2.493, 5.051, 10.346, 21.307, 44.127]
time_reduce_rate = [(local_time[i] - offload_time[i]) / local_time[i] * 100 for i in range(8)]
local_power = [0.23, 0.72, 0.76, 0.89, 1.14, 3.56, 5.77, 10.22]
offload_power = [0.17, 0.19, 0.22, 0.63, 0.74, 1.37, 1.85, 2.7]
power_reduce_rate = [(local_power[i] - offload_power[i]) / local_power[i] * 100 for i in range(8)]

fig = plt.figure()
ax1 = fig.add_subplot(111)
bar_x = list(range(len(bar_name_list)))
total_width, n = 0.9, 3
width = total_width / n
ax1.bar(bar_x, local_time, width=width, label='Local', tick_label=bar_name_list, ec='k')
for i in range(len(bar_x)):
    bar_x[i] = bar_x[i] + width
ax1.bar(bar_x, offload_time, width=width, label='Offload', ec='k')
ax1.set_xlabel('Computing Task (M, N)')
ax1.set_ylabel('Task completion time (seconds)')
ax1.set_ylim([0, 80])
plt.yticks()

ax2 = ax1.twinx()
ax2.plot(bar_x, time_reduce_rate, 'r', marker='*' , ls='-', label='Reduction Rate')
ax2.set_ylim([0, 40])
ax2.set_ylabel("Time Reduce Percentage (%)")

ax1.legend(loc=2)
ax2.legend()
fig.savefig('times.svg', dpi=600, format='svg')


fig = plt.figure()
ax1 = fig.add_subplot(111)
bar_x = list(range(len(bar_name_list)))
total_width, n = 0.9, 3
width = total_width / n
ax1.bar(bar_x, local_power, width=width, label='Local', tick_label=bar_name_list, ec='k')
for i in range(len(bar_x)):
    bar_x[i] = bar_x[i] + width
ax1.bar(bar_x, offload_power, width=width, label='Offload', ec='k')
ax1.set_xlabel('Computing Task (M, N)')
ax1.set_ylabel('Task Power Consumption (mAh)')
ax1.set_ylim([0, 12])
plt.yticks()

ax2 = ax1.twinx()
ax2.plot(bar_x, power_reduce_rate, 'r', marker='*' , ls='-', label='Reduction Rate')
ax2.set_ylim([0, 100])
ax2.set_ylabel("Power Reduce Percentage (%)")

ax1.legend(loc=2)
ax2.legend()
fig.savefig('power.svg', dpi=600, format='svg')
