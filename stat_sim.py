import numpy as np
import itertools
import matplotlib.pyplot as plt
from math import floor
import sys


def average_roll(rolls):
    avg_d = np.sum(list(itertools.product(*rolls[0])), axis=1)
    avg_p = np.product(list(itertools.product(*rolls[1])), axis=1)
    new_d = np.unique(avg_d)
    new_p = [sum(avg_p[avg_d == new_d[i]]) for i in range(len(new_d))]
    return new_d, new_p


# 3d6 + 4
# roll = 3
# rolled = 6
# fix = 4
def proba_roll(roll, rolled, drop_low=False, res_sum=True, proba=True, fix=0):
    # generator
    rolls = itertools.product(
        range(1+fix, rolled+1+fix),
        repeat=roll)
    # list of list
    rolls = np.array([list(tup) for tup in rolls])
    if drop_low:
        rolls[range(len(rolls)), rolls.argmin(axis=1)] = 0
    if res_sum:
        rolls = np.sum(rolls, axis=1)
        res = list(np.unique(rolls, return_counts=True))
    else:
        rolls = np.sort(rolls)
        res = list(np.unique(rolls, return_counts=True, axis=0))
    if proba:
        res[1] = res[1] / res[1].sum()
    return res[0], res[1]


def plot(*data, title='title', xlabel='xaxis', ylabel='probability'):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    for v, k in data:
        ax.plot(*v, label=k)
    ax.legend()
    plt.show()


def plot_normal_vs_drop():
    normal = (proba_roll(3, 6), '3d6')
    drop_lowest = (proba_roll(4, 6, drop_low=True),
                   '4d6 drop low')
    plot(normal, drop_lowest,
         title='stat comparison', xlabel='result')
    plt.show()


def average_6():
    normal = (average_roll(
        list(zip(*[proba_roll(3, 6) for i in range(6)]))),
        '3d6')
    drop_lowest = (average_roll(
        list(zip(*[proba_roll(4, 6, drop_low=True) for i in range(6)]))),
        '4d6 drop low')
    plot(normal, drop_lowest,
         title='stat comparison', xlabel='result')
    plt.show()


def ask(asked=[(1, 3, 4), (3, 5, 6), (6, 6, 6),
               (2, 3, 5), (3, 3, 4), (2, 1, 1)],
        method='3d6', res_sum=False, sum_all=False):
    if sum_all:
        proba = True
    else:
        proba = False
        asked = np.sort(np.array(asked))
    if method == '3d6':
        stat = proba_roll(3, 6, res_sum=res_sum, proba=proba)
    elif method == '4d6':
        if res_sum:
            stat = proba_roll(4, 6, res_sum=res_sum, proba=proba, drop_low=True)
        else:
            stat = proba_roll(4, 6, res_sum=res_sum, proba=proba)
    else:
        sys.exit('wrong method for dice')
    if sum_all and res_sum:
        avg = average_roll(list(zip(*[stat for i in range(6)])))
        res = avg[1][avg[0] == asked][0]
        print(res, '%')
    else:
        if res_sum:
            res = [stat[1][np.where((stat[0] == i))[0]] for i in asked]
        else:
            res = [stat[1][np.where((stat[0] == i).all(axis=1))[0]]
                   for i in asked]
        res = np.sum(res)
        total = (sum(stat[1])*len(asked))
        print(res, 'chances out of', total)
        print(100*res/total, '%')


if __name__ == '__main__':
    plot_normal_vs_drop()


def facto(x):
    if x == 0:
        return 1
    else:
        return np.product(range(1, x+1))


def c(n, k):
    return facto(n) / (facto(k) * facto(n - k))


def test(r, n, s):
    ran = list(range(0, floor(((r-n)/s)+1)))
    return 1/(s**n) * sum([((-1)**k) * c(n, k) * c(r - 1 - (k*s), n-1) for k in ran])

    
