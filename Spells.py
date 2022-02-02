import numpy as np
import itertools
import matplotlib.pyplot as plt


DC_TYPES = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
DAMAGE_TYPES = ['Fire', 'Thunder', 'Cold', 'Lightning', 'Acid', 'Poison',
                'Necrotic', 'Radiant', 'Bludgeo', 'Slash', 'Stab', 'Psychic']


# target:
# 0 = aoe
# 1-XX = number of target
class Damage:
    def __init__(self, rolls, damage, damage_type, fix=0, hit=False, dc=False,
                 dc_type='', turn=False, target=1, upcast=False,
                 upcast_per_level=0, rebound=0):
        self.rolls = rolls
        self.damage = damage
        self.damage_type = damage_type
        self.fix = fix
        self.hit = hit
        self.dc = dc
        self.dc_type = dc_type
        self.turn = turn
        self.target = target

    def get_damage(self):
        rolls = itertools.product(range(1+self.fix, self.damage+1+self.fix),
                                  repeat=self.rolls)
        res = np.unique(np.sum(list(rolls),
                               axis=1),
                        return_counts=True)
        return res[0], res[1] / res[1].sum()


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

    def roll_on_hit(self):
        dmg = []
        for d in self.damages:
            if d.hit:
                dmg.append(d.get_damage())
        return Spells.average_damages(list(zip(*dmg)))
