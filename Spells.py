import numpy as np
import itertools
import matplotlib.pyplot as plt
from math import floor

DC_TYPES = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
DAMAGE_TYPES = ['Fire', 'Thunder', 'Cold', 'Lightning', 'Acid', 'Poison',
                'Necrotic', 'Radiant', 'Bludgeo', 'Slash', 'Stab', 'Psychic']


# target:
# 0 = aoe
# 1-XX = number of target
class Damage:
    def __init__(self, roll, damage, damage_type, fix=0, hit=False, dc=False,
                 dc_type='', dc_fail=0, turn=False, target=1,
                 upcast_per_level=0, rebound=0):
        self.roll = roll
        self.damage = damage
        self.damage_type = damage_type
        self.fix = fix
        self.hit = hit
        self.dc = dc
        self.dc_type = dc_type
        self.turn = turn
        self.target = target
        self.upcast_per_level = upcast_per_level

    def get_damage(self, upcast=0):
        rolls = itertools.product(
            range(1+self.fix, self.damage+1+self.fix),
            repeat=self.roll + floor(upcast*self.upcast_per_level))
        res = np.unique(np.sum(list(rolls),
                               axis=1),
                        return_counts=True)
        return res[0], res[1] / res[1].sum()

    def is_hit(damage):
        return damage.hit

    def is_dc(damage):
        return damage.dc


class Spells:
    def __init__(self, name, level, damages=[]):
        self.name = name
        self.level = level
        self.damages = damages

    def average_damages(damages):
        avg_d = np.sum(list(itertools.product(*damages[0])), axis=1)
        avg_p = np.product(list(itertools.product(*damages[1])), axis=1)
        new_d = np.unique(avg_d)
        new_p = [sum(avg_p[avg_d == new_d[i]]) for i in range(len(new_d))]
        return new_d, new_p

    def roll_on_hit(self, upcast=0):
        return self.roll_all(Damage.is_hit, upcast)

    def roll_on_dc(self, upcast=0):
        return self.roll_all(Damage.is_dc, upcast)

    def roll_all(self, cond=lambda x: True, upcast=0):
        dmg = []
        for d in self.damages:
            if cond(d):
                dmg.append(d.get_damage(upcast))
        if len(dmg) == 0:
            return ([], [])
        else:
            return Spells.average_damages(list(zip(*dmg)))


def test():
    fig, ax = plt.subplots()
    ax.set_title('DND spell damage comparison')
    ax.set_ylabel('percentage')
    ax.set_xlabel('damage')
    burning_hands = Spells('Burning Hands', 1, [Damage(
        3, 6, 'Fire', dc=True, dc_type='DEX', dc_fail=0.5,
        upcast_per_level=1)])
    ice_knife = Spells('Ice Knife', 1, [
        Damage(1, 10, 'Piercing', hit=True),
        Damage(2, 6, 'Ice', dc=True, upcast_per_level=1)])
    fireball = Spells('Fireball', 3, [Damage(
        8, 6, 'Fire', dc=True, dc_type='DEX', dc_fail=0.5,
        upcast_per_level=1)])
    ax.plot(*burning_hands.roll_on_dc(upcast=2), label=burning_hands.name)
    ax.plot(*ice_knife.roll_all(upcast=2), label=ice_knife.name)
    ax.plot(*fireball.roll_on_dc(upcast=0), label=fireball.name)
    ax.legend()
    plt.show()
