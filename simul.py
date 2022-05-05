import d20
from math import floor
from abc import ABC, abstractmethod


class Stat:
    name_stats = ['str', 'int', 'cha', 'dex', 'wis', 'con']
    default_value = 10

    def __init__(self, mod=True, **kwargs):
        if mod:
            self.value = Stat(mod=False, **kwargs)
            for atr in Stat.name_stats:
                setattr(self, atr, floor((getattr(self.value, atr)-10)/2))

        else:
            for atr in Stat.name_stats:
                setattr(self, atr,
                        kwargs[atr] if atr in kwargs else Stat.default_value)


class Entity(ABC):
    def __init__(self, level, name,
                 stats, ac=0, hp=0):
        self.hp = hp
        self.max_hp = hp
        self.ac = ac
        self.level = level
        self.stats = Stat(**stats)
        self.name = name
        self.proficiency = int((level-1)/4)+2
        self.compute_attr()

    @abstractmethod
    def compute_attr():
        pass

    def main_attack(self, target):
        if len(self.weapons) >= 0:
            return self.attack(self.weapons[0], target)
        else:
            return f"{self.name} has no weapon"

    def attack(self, weapon, target):
        to_hit, crit, expr = self.to_hit(weapon)
        msg = f"{self.name} attacks {target.name}"
        msg += f"\n{self.name} rolls {expr}"
        if crit == 1 or target.is_hit(to_hit):
            damage, elem = weapon.roll_damage(crit)
            res = target.lose_hp(damage, elem)
            msg += f"\n{self.name} has touched {target.name}"
            msg += "\n" + res
        else:
            msg += f"\n{self.name} has missed {target.name}"
        return msg

    def to_hit(self, weapon):
        roll = d20.roll(f"d20+{self.proficiency+self.stats.str}")
        return roll.total, roll.crit, roll.result

    def is_hit(self, to_hit):
        return to_hit >= self.ac

    def lose_hp(self, damage, elem):
        self.hp -= damage
        msg = f"{self.name} has lost {damage} hp"
        if self.hp <= 0:
            msg += f"\n{self.name} is unconscious"
        return msg


class Class(Entity):
    def __init__(self, level, name,
                 stats):
        super().__init__(level, name,
                         stats)

    def compute_attr(self):
        self.ac = 10 + self.stats.dex

    def equip_weapon(self, weapon):
        self.weapons.append(weapon)


class Warrior(Class):
    def __init__(self, level, name, stats):
        super().__init__(level, name,
                         stats)
        self.weapons = []

    def compute_attr(self):
        self.hp = 10 + 6*(self.level-1) + self.level * self.stats.con
        self.max_hp = self.hp


class Weapons:
    def __init__(self, name, bonus, damage, crit_damage, elem):
        self.name = name
        self.bonus = bonus
        #  2d8+5
        self.damage = damage
        self.crit_damage = crit_damage
        self.elem = elem

    def roll_damage(self, crit):
        if crit == 1:
            to_roll = self.crit_damage
        else:
            to_roll = self.damage
        return d20.roll(to_roll).total, self.elem


# 0 = Common
# 1 = Uncommon
# 2 = Rare
# 3 = Very rare
# 4 = Legendary
class Item:
    def __init__(self, name, price, rarity,
                 attunement=False, magic=False, consumable=False):
        self.name = name
        self.price = price
        self.rarity = rarity
        self.attunement = attunement
        self.magic = magic
        self.consumable = consumable


class Consumable(Item, ABC):
    def __init__(self, name, price, rarity, charge):
        super().__init__(name, price, rarity, consumable=True)
        self.charge = charge

    @abstractmethod
    def consume(self, target):
        pass


class Healing_Potion(Consumable):
    def __init__(self):
        super().__init__('Healing potion', 50, 0, 1)

    def consume(self, target):
        roll = d20.roll("2d4+2")
        target.hp = min(target.hp+roll.total, target.max_hp)
        return f"{target.name} has consumed a {self.name}" \
            + f"and regained {roll} hp"


ls = Weapons("long-sword", 0, "1d8", "2d8", "slashing")
gs = Weapons("great-sword", 0, "2d6", "4d6", "slashing")

w1 = Warrior(1, 'jon', {'str': 16, 'con': 14, 'dex': 12})
w2 = Warrior(1, 'bob', {'str': 18, 'con': 12})
w1.equip_weapon(gs)
w2.equip_weapon(ls)


while w1.hp >= 0 and w2.hp >= 0:
    print(w1.main_attack(w2))
    print(' ')
    if w2.hp >= 0:
        print(w2.main_attack(w1))
    print('--')
