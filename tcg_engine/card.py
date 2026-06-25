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
    
    def attach_energy(self, energy_type):
        self.energy_attached.append(energy_type)

    def evolve_into(self, new_form):
        new_form.energy_attached = self.energy_attached
        return new_form
    
class Attack:
    def __init__(self, name, damage, energy_cost):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
    
    def can_use(self, energy_attached):
        available = energy_attached.copy()
        cost_copy = self.energy_cost.copy()

        # First pass: match specific (non-Colorless) costs exactly
        specific_costs = [c for c in cost_copy if c != "Colorless"]
        for cost in specific_costs:
            if cost in available:
                available.remove(cost)
                cost_copy.remove(cost)
            else:
                return False

        # Second pass: remaining cost must all be Colorless, pay with ANY leftover energy
        colorless_needed = cost_copy.count("Colorless")
        if len(available) < colorless_needed:
            return False

        return True