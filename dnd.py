import numpy as np
import itertools
import matplotlib.pyplot as plt


def get_damage(r, d, fix=0):
    rolls = [j for i in range(len(r)) for j in [range(1, 1+d[i])]*r[i]]
    res = np.unique(np.sum(list(itertools.product(*rolls)),
                           axis=1),
                    return_counts=True)
    return res[0]+fix, res[1] / res[1].sum() * 100


def lv_3():
    fireball = get_damage([8], [6])
    chaosball = get_damage([2, 1], [20, 6])
    fig, ax = plt.subplots()
    ax.set_title('DND lv 3 spell damage comparison')
    ax.plot(*fireball, label='fireball--DEX 1/2--Fire')
    # ax.plot(*chaosball, label="Kai's chaos ball")
    ax.legend()


def lv_2():
    fireball = get_damage([8], [6])
    chaosball = get_damage([2, 1], [20, 6])
    fig, ax = plt.subplots()
    ax.set_title('DND lv 2 spell damage comparison')
    ax.plot(*fireball, label='fireball')
    ax.plot(*chaosball, label="Kai's chaos ball")
    ax.legend()


def lv_1():
    burning_hands = get_damage([3], [6])
    catapult = get_damage([3], [8])
    chaos_bolt = get_damage([2, 1], [8, 6])
    chromatic_orb = get_damage([3], [8])
    ice_knife = get_damage([1, 2], [10, 6])
    magic_missile = get_damage([3], [4], 1)
    rays_of_sickness = get_damage([2], [8])
    thunderwave = get_damage([2], [8])
    witch_bolt = get_damage([1], [12])
    fig, ax = plt.subplots()
    ax.set_title('DND lv 1 spell damage comparison')
    ax.set_ylabel('percentage')
    ax.set_xlabel('damage')
    ax.plot(*burning_hands, label='burning hands  DEX 1/2  Fire')
    ax.plot(*catapult, label="catapult  DEX 0  Bludgeonning")
    ax.plot(*chaos_bolt, label="chaos bolt  Hit  Random")
    ax.plot(*chromatic_orb, label="chromatic orb  Hit  Elem")
    ax.plot(*ice_knife, label="ice_knife  HIT/DEX 0  Ice")
    ax.plot(*magic_missile, label="magic missile  100%  Force")
    ax.plot(*rays_of_sickness, label="rays of sickness  CON 0  Poison")
    ax.plot(*thunderwave, label="thunderwave  CON 1/2  Thunder")
    ax.plot(*witch_bolt, label="witch bolt  Hit  Lighting")
    ax.legend()
