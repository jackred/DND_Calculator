import numpy as np
import itertools
import matplotlib.pyplot as plt
from math import floor

DC_TYPES = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
DAMAGE_TYPES = ['Fire', 'Thunder', 'Cold', 'Lightning', 'Acid', 'Poison',
                'Necrotic', 'Radiant', 'Bludgeon', 'Slash', 'Stab', 'Psychic',
                'Random']


def average_damages(damages):
    avg_d = np.sum(list(itertools.product(*damages[0])), axis=1)
    avg_p = np.product(list(itertools.product(*damages[1])), axis=1)
    new_d = np.unique(avg_d)
    new_p = [sum(avg_p[avg_d == new_d[i]]) for i in range(len(new_d))]
    return new_d, new_p


# target:
# 0 = aoe
# 1-XX = number of target
class Damage:
    def __init__(self, roll, damage, damage_type, fix=0, hit=False, dc=False,
                 dc_type='', dc_fail=0, turn_roll=0, target=1,
                 upcast_per_level=0, rebound=False, rebound_spell=[],
                 new=False):
        self.roll = roll
        self.damage = damage
        self.damage_type = damage_type
        self.fix = fix
        self.hit = hit
        self.dc = dc
        self.dc_type = dc_type
        self.turn_roll = turn_roll
        self.target = target
        self.upcast_per_level = upcast_per_level
        self.rebound = rebound
        self.new = new
        self.rebound_spell = []
        for i in rebound_spell:
            if i == 'self':
                self.rebound_spell.append(self)
            elif i is not None:
                self.rebound_spell.append(i)

    def get_damage(self, upcast=0, turn=0, rebound=0):
        rolls = itertools.product(
            range(1+self.fix, self.damage+1+self.fix),
            repeat=self.roll
            + floor(upcast*self.upcast_per_level)
            + floor(turn*self.turn_roll))
        res = list(np.unique(np.sum(list(rolls),
                                    axis=1),
                             return_counts=True))
        if rebound > 0 and self.rebound:
            dmg_r = []
            for spell in self.rebound_spell:
                dmg_r.append(spell.get_damage(rebound=rebound-1, upcast=upcast,
                                              turn=turn))
            new_d = average_damages(list(zip(*dmg_r)))
            for i in range(1, self.damage+1):
                idx = np.where(res[0] == (i+i))[0][0]
                res[1][idx] -= 1
                res[1] = np.append(res[1], new_d[1])
                res[0] = np.append(res[0], (i+i)+new_d[0])
                #  new rebound chaos ball
                if self.new:
                    idx = np.where(res[0] == (i+((10+i) % 20)))[0][0]
                    res[1][idx] -= 1
                    res[1] = np.append(res[1], new_d[1])
                    res[0] = np.append(res[0], (i+((10+i) % 20))+new_d[0])
        print(res)
        return res[0], res[1] / res[1].sum()

    def is_hit(damage):
        return damage.hit

    def is_dc(damage):
        return damage.dc


class Spells:
    def __init__(self, name, level, damages=[], range_s='touch',
                 cast='action'):
        self.name = name
        self.level = level
        self.damages = damages
        self.cast = cast
        self.range_s = range_s

    def roll_on_hit(self, upcast=0, turn=0, rebound=0):
        return self.roll_all(Damage.is_hit, upcast, turn, rebound)

    def roll_on_dc(self, upcast=0, turn=0, rebound=0):
        return self.roll_all(Damage.is_dc, upcast, turn, rebound)

    def roll_all(self, cond=lambda x: True, upcast=0, turn=0, rebound=0):
        dmg = []
        for d in self.damages:
            if cond(d):
                dmg.append(d.get_damage(upcast, turn, rebound))
        if len(dmg) == 0:
            return ([], [])
        else:
            return average_damages(list(zip(*dmg)))


def test():
    fig, ax = plt.subplots()
    ax.set_title('DND lv 1 spell damage comparison')
    ax.set_ylabel('probability')
    ax.set_xlabel('damage')
    burning_hands = Spells('Burning Hands', 1, [Damage(
        3, 6, 'Fire', dc=True, dc_type='DEX', dc_fail=0.5,
        upcast_per_level=1)])
    ice_knife = Spells('Ice Knife', 1, [
        Damage(1, 10, 'Piercing', hit=True),
        Damage(2, 6, 'Ice', dc=True, upcast_per_level=1)])
    witch_bolt = Spells('Witch Bolt', 1, [
        Damage(1, 12, 'Lightning', hit=True, turn_roll=1,
               upcast_per_level=1)])
    arms_of_hadar = Spells('Arms of Hadar', 1, [
        Damage(2, 6, 'Necrotic', dc=True, dc_type='Strength', dc_fail=0.5,
               upcast_per_level=1)])
    catapult = Spells('Catapult', 1, [
        Damage(3, 8, 'Bludgeon', dc=True, dc_type='DEX')])
    cbd6 = Damage(1, 6, 'Random', hit=True, upcast_per_level=1)
    chaos_bolt = Spells('Chaos Bolt', 1, [
        Damage(2, 8, 'Random', hit=True, upcast_per_level=0,
               rebound_spell=['self', cbd6], rebound=True), cbd6])
    chromatic_orb = Spells('Chromatic Orb', 1, [
        Damage(3, 8, 'Random', hit=True, upcast_per_level=1)])
    dissonant_whispers = Spells('Dissonant Whispers', 1, [Damage(
        3, 6, 'Psychic', dc=True, dc_type='WIS', dc_fail=0.5,
        upcast_per_level=1)])
    earth_tremor = Spells('Earth Tremor', 1, [Damage(
        1, 6, 'Bludgeon', dc=True, dc_type='DEX', dc_fail=0,
        upcast_per_level=1)])
    frost_fingers = Spells('Frost Fingers', 1, [Damage(
        2, 8, 'Ice', dc=True, dc_type='CON', dc_fail=0.5,
        upcast_per_level=1)])
    guiding_bolt = Spells('Guiding Bolt', 1, [
        Damage(4, 6, 'Radiant', hit=True, upcast_per_level=1)])
    hellish_rebuke = Spells('Hellish Rebuke', 1, cast='reaction', damages=[
        Damage(4, 6, 'Fire',  dc=True, dc_type='DEX', upcast_per_level=1)])
    inflict_wounds = Spells('Inflict Wound', 1, [
        Damage(3, 10, 'Necrotic', hit=True, upcast_per_level=1)])
    magic_missile = Spells('Magic Missile', 1, [
        Damage(3, 4, 'Force', fix=1, hit=True, upcast_per_level=1)])
    tashas_caustic_brew = Spells("Tasha's Caustic Brew", 1, [
        Damage(2, 4, 'Acid', dc=True, dc_type='DEX', turn_roll=2,
               upcast_per_level=2)])
    thunderwave = Spells('Thunderwave', 1, [
        Damage(2, 8, 'Thunder', dc=True, dc_type='CON', dc_fail=0.5,
               upcast_per_level=1)])
    ax.plot(*burning_hands.roll_on_dc(upcast=0), label=burning_hands.name)
    ax.plot(*ice_knife.roll_all(upcast=0), label=ice_knife.name)
    ax.plot(*witch_bolt.roll_on_hit(upcast=0), label=witch_bolt.name)
    ax.plot(*witch_bolt.roll_on_hit(upcast=0, turn=2),
            label=witch_bolt.name+' 2 turn')
    ax.plot(*catapult.roll_on_dc(upcast=0, turn=0), label=catapult.name)
    ax.plot(*arms_of_hadar.roll_on_dc(upcast=0, turn=2),
            label=arms_of_hadar.name)
    ax.plot(*chaos_bolt.roll_on_hit(upcast=0, rebound=0),
            label=chaos_bolt.name)
    ax.plot(*chaos_bolt.roll_on_hit(upcast=0, rebound=1),
            label=chaos_bolt.name + ' 1 rebound')
    ax.plot(*chromatic_orb.roll_on_hit(upcast=0),
            label=chromatic_orb.name)
    ax.plot(*dissonant_whispers.roll_on_dc(upcast=0),
            label=dissonant_whispers.name)
    ax.plot(*earth_tremor.roll_on_dc(upcast=0),
            label=earth_tremor.name)
    ax.plot(*frost_fingers.roll_on_dc(upcast=0),
            label=frost_fingers.name)
    ax.plot(*guiding_bolt.roll_on_hit(upcast=0),
            label=guiding_bolt.name)
    ax.plot(*hellish_rebuke.roll_on_dc(upcast=0),
            label=hellish_rebuke.name)
    ax.plot(*inflict_wounds.roll_on_hit(upcast=0),
            label=inflict_wounds.name)
    ax.plot(*magic_missile.roll_on_hit(upcast=0),
            label=magic_missile.name)
    ax.plot(*tashas_caustic_brew.roll_on_dc(upcast=0),
            label=tashas_caustic_brew.name)
    ax.plot(*tashas_caustic_brew.roll_on_dc(upcast=0, turn=2),
            label=tashas_caustic_brew.name+' 2 turn')
    ax.plot(*thunderwave.roll_on_dc(upcast=0),
            label=thunderwave.name)
    ax.legend()
    plt.show()


def lv2():
    fig, ax = plt.subplots()
    ax.set_title('DND lv 2 spell damage comparison')
    ax.set_ylabel('probability')
    ax.set_xlabel('damage')
    fireball = Spells('Fireball', 3, [Damage(
        8, 6, 'Fire', dc=True, dc_type='DEX', dc_fail=0.5,
        upcast_per_level=1)])
    cbd6_hit = Damage(3, 6, 'Random', hit=True, upcast_per_level=1)
    cbd8 = Damage(2, 8, 'Random', hit=True, upcast_per_level=0,
                  rebound_spell=['self', cbd6_hit], rebound=True)
    chaos_ball = Spells('Chaos Ball', 3, [
        Damage(2, 20, 'Random', dc=True, dc_type='DEX', upcast_per_level=0,
               rebound_spell=[cbd8, cbd6_hit], rebound=True),
        Damage(1, 6, 'Random', dc=True, dc_type='DEX', upcast_per_level=1)])
    ax.plot(*fireball.roll_on_dc(upcast=0), label=fireball.name)
    ax.plot(*chaos_ball.roll_on_dc(upcast=0, rebound=1),
            label=chaos_ball.name)
    ax.legend()
    plt.show()


def lv3():
    fig, ax = plt.subplots()
    ax.set_title('DND lv 3 spell damage comparison')
    ax.set_ylabel('probability')
    ax.set_xlabel('damage')
    fireball = Spells('Fireball', 3, [Damage(
        8, 6, 'Fire', dc=True, dc_type='DEX', dc_fail=0.5,
        upcast_per_level=1)])
    cbd6_hit = Damage(3, 6, 'Random', hit=True, upcast_per_level=1)
    cbd8 = Damage(2, 8, 'Random', hit=True, upcast_per_level=0,
                  rebound_spell=['self', cbd6_hit], rebound=True)
    chaos_ball = Spells('Chaos Ball', 3, [
        Damage(2, 20, 'Random', dc=True, dc_type='DEX', upcast_per_level=0,
               rebound_spell=[cbd8, cbd6_hit], rebound=True),
        Damage(1, 6, 'Random', dc=True, dc_type='DEX', upcast_per_level=1)])
    chaos_ball_2 = Spells('Chaos Ball New', 3, [
        Damage(2, 20, 'Random', dc=True, dc_type='DEX', upcast_per_level=0,
               rebound_spell=[cbd8, cbd6_hit], rebound=True, new=True),
        Damage(1, 6, 'Random', dc=True, dc_type='DEX', upcast_per_level=1)])
    ax.plot(*fireball.roll_on_dc(upcast=0), label=fireball.name)
    ax.plot(*chaos_ball.roll_on_dc(upcast=0, rebound=1),
            label=chaos_ball.name+' 1 rebound')
    ax.plot(*chaos_ball.roll_on_dc(upcast=0, rebound=0),
            label=chaos_ball.name)
    ax.plot(*chaos_ball_2.roll_on_dc(upcast=0, rebound=1),
            label=chaos_ball_2.name+' 1 rebound')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    #test()
    lv3()
