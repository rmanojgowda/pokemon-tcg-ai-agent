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

    def execute_attack(self, attacker, attack, defender, defender_board, attacker_board):
        if not attack.can_use(attacker.energy_attached):
            return False

        damage = attack.damage
        if defender.weakness == attacker.ptype:
            damage = damage * 2

        defender.damage_taken += damage

        if defender.is_knocked_out():
            defender_board.knock_out_active()
            attacker_board.prizes_remaining -= 1

        return True
    
    def check_winner(self):
        if self.opponent_board.prizes_remaining <= 0:
            return "player"
        if self.player_board.prizes_remaining <= 0:
            return "opponent"

        if self.opponent_board.active is None and len(self.opponent_board.bench) == 0:
            return "player"
        if self.player_board.active is None and len(self.player_board.bench) == 0:
            return "opponent"

        return None
    
    def simulate_simple_battle(self, max_turns=20):
        for turn in range(1, max_turns + 1):
            self.start_new_turn()
            print(f"\n--- Turn {turn} ---")

            attacker_board = self.player_board if turn % 2 != 0 else self.opponent_board
            defender_board = self.opponent_board if turn % 2 != 0 else self.player_board

            attacker = attacker_board.active
            defender = defender_board.active

            if attacker is None or defender is None:
                print("One side has no active Pokemon. Stopping.")
                break

            usable_attack = None
            for attack in attacker.attacks:
                if attack.can_use(attacker.energy_attached):
                    usable_attack = attack
                    break

            if usable_attack is None:
                self.attach_energy_to_pokemon(attacker, attacker.ptype)
                print(f"{attacker.name} attached energy. Energy now: {attacker.energy_attached}")
            else:
                self.execute_attack(attacker, usable_attack, defender, defender_board, attacker_board)
                print(f"{attacker.name} used {usable_attack.name} on {defender.name}!")
                print(f"{defender.name} HP: {defender.current_hp()}")

            winner = self.check_winner()
            if winner is not None:
                print(f"\n🏆 {winner.upper()} WINS on turn {turn}!")
                return winner

        print("\nMax turns reached, no winner.")
        return None