from tcg_engine.board import Board


class Game:
    def __init__(self):
        self.player_board = Board()
        self.opponent_board = Board()
        self.turn_number = 0
        self.energy_attached_to_this_turn = False

    def attach_energy_to_pokemon(self, pokemon, energy_type):
        if self.energy_attached_to_this_turn:
            return False
        pokemon.attach_energy(energy_type)
        self.energy_attached_to_this_turn = True
        return True

    def start_new_turn(self):
        self.turn_number += 1
        self.energy_attached_to_this_turn = False

    def execute_attack(self, attacker, attack, defender):
        if not attack.can_use(attacker.energy_attached):
            return False

        damage = attack.damage
        if defender.weakness == attacker.ptype:
            damage = damage * 2

        defender.damage_taken += damage
        return True