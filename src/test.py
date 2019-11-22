# -*- encoding: utf-8 -*-
#
# comment
#
# 19-11-21 leo : Init

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def demo1():
    mu, sigma = 3000, 256
    sampleNo = 1000
    s = np.random.normal(mu, sigma, sampleNo)

    plt.hist(s, bins=100, normed=True)
    plt.show()

demo1()