from tcg_engine.card import Pokemon, Attack
from tcg_engine.board import Board
from tcg_engine.game import Game

# ============================================
# CARD CLASS TESTS - Pokemon and Attack setup
# ============================================
print("=== CARD TESTS ===")

thunder_shock = Attack("Thunder Shock", 30, ["Lightning", "Lightning"])
tackle = Attack("Tackle", 20, ["Colorless"])

pikachu = Pokemon("Pikachu", 60, "Lightning", "Fighting", [thunder_shock], 1)
squirtle = Pokemon("Squirtle", 50, "Water", "Lightning", [tackle], 1)
bulbasaur = Pokemon("Bulbasaur", 50, "Grass", "Fire", [tackle], 1)

# ============================================
# BOARD CLASS TESTS
# ============================================
print("\n=== BOARD TESTS ===")

board = Board()
board.set_active(pikachu)
board.add_to_bench(squirtle)
board.add_to_bench(bulbasaur)

print("Active : ", board.active.name)
print("Bench : ", [p.name for p in board.bench])
print("Prizes remaining : ", board.prizes_remaining)

board.knock_out_active()
print("\nAfter knocking out :")
print("Active : ", board.active)
print("Discard pile : ", [p.name for p in board.discard_pile])

result = board.promote_from_bench(0)
print("\nPromotion successful ? ", result)
print("Active :", board.active.name)
print("Bench : ", [p.name for p in board.bench])

print("\nCurrent HP :", pikachu.current_hp())

pikachu.damage_taken = 20
print("After 20 damage, HP :", pikachu.current_hp())

print("Is knocked out ?", pikachu.is_knocked_out())

print("Can use thunder shock with no energy", thunder_shock.can_use([]))
print("Can use thunder shock with 1 energy", thunder_shock.can_use(["Lightning"]))
print("Can use thunder shock with 2 energy", thunder_shock.can_use(["Lightning", "Lightning"]))

# ============================================
# GAME CLASS TESTS - Energy attachment rules
# ============================================
print("\n\n=== GAME TESTS ===")

game = Game()
game.player_board.set_active(pikachu)

print("Turn number:", game.turn_number)

result1 = game.attach_energy_to_pokemon(pikachu, "Lightning")
print("\nFirst attach attempt:", result1)
print("Pikachu energy:", pikachu.energy_attached)

result2 = game.attach_energy_to_pokemon(pikachu, "Lightning")
print("\nSecond attach attempt (same turn):", result2)
print("Pikachu energy:", pikachu.energy_attached)

game.start_new_turn()
print("\nAfter start_new_turn, turn number:", game.turn_number)

result3 = game.attach_energy_to_pokemon(pikachu, "Lightning")
print("\nThird attach attempt (new turn):", result3)
print("Pikachu energy:", pikachu.energy_attached)

print("\nCan use Thunder Shock now?", thunder_shock.can_use(pikachu.energy_attached))