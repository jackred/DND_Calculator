import d20


class Entity:
    def __init__(self, hp, level, ac, name,
                 strength, constitution, dexterity):
        self.hp = hp
        self.ac = ac
        self.name = name
        self.str = strength
        self.con = constitution
        self.dex = dexterity
        self.proficiency = int((level-1)/4)+2

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
        roll = d20.roll(f"d20+{self.proficiency+self.str}")
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
    def __init__(self, hp, level, name,
                 strength, constitution, dexterity):
        ac = 10 + dexterity
        super().__init__(hp, level, ac, name,
                         strength, constitution, dexterity)


class Warrior(Class):
    def __init__(self, level, name, strength, constitution, dexterity):
        hp = 10 + 6*(level-1) + level * constitution
        super().__init__(hp, level, name,
                         strength, constitution, dexterity)
        self.weapons = []

    def equip_weapon(self, weapon):
        self.weapons.append(weapon)


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


ls = Weapons("long-sword", 0, "1d8", "2d8", "slashing")
gs = Weapons("great-sword", 0, "2d6", "4d6", "slashing")

w1 = Warrior(1, 'jon', 3, 2, 1)
w2 = Warrior(1, 'bob', 4, 0, 1)
w1.equip_weapon(gs)
w2.equip_weapon(ls)


while w1.hp >= 0 and w2.hp >= 0:
    print(w1.main_attack(w2))
    print(' ')
    if w2.hp >= 0:
        print(w2.main_attack(w1))
    print('--')
