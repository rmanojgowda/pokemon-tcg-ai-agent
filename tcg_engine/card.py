class Pokemon:
    def __init__(self, name, hp, ptype, weakness, attacks, retreat_cost):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.ptype = ptype
        self.weakness = weakness
        self.attacks = attacks
        self.retreat_cost = retreat_cost
        self.energy_attached = []
        self.damage_taken = 0

    def current_hp(self):
        return self.max_hp - self.damage_taken
    
    def is_knocked_out(self):
        return self.current_hp() <= 0
    
class Attack:
    def __init__(self, name, damage, energy_cost):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
    
    def can_use(self, energy_attached):
        cost_copy = self.energy_cost.copy()
        for energy in energy_attached:
            if energy in cost_copy:
                cost_copy.remove(energy)
        return len(cost_copy) == 0