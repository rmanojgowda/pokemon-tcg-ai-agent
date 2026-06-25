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

# ============================================
# ATTACK EXECUTION TESTS - Damage + Weakness + Prizes
# ============================================
print("\n\n=== ATTACK EXECUTION TESTS ===")

game2 = Game()

geodude = Pokemon("Geodude", 60, "Fighting", "Water", [tackle], 1)
fresh_pikachu = Pokemon("Pikachu", 60, "Lightning", "Fighting", [thunder_shock], 1)
fresh_squirtle = Pokemon("Squirtle", 50, "Water", "Lightning", [tackle], 1)

# Set up boards properly
game2.player_board.set_active(fresh_squirtle)
game2.opponent_board.set_active(geodude)

print("Player prizes remaining (start):", game2.player_board.prizes_remaining)
print("Opponent prizes remaining (start):", game2.opponent_board.prizes_remaining)

# Test 1: Not enough energy - should fail
print("\n--- Test 1: Attack with insufficient energy ---")
fresh_pikachu.attach_energy("Lightning")
result = game2.execute_attack(fresh_pikachu, thunder_shock, geodude, game2.opponent_board, game2.player_board)
print("Attack succeeded?", result)
print("Geodude damage taken:", geodude.damage_taken)

# Test 2: Enough energy, no weakness - normal damage
print("\n--- Test 2: Attack with enough energy, no weakness ---")
fresh_pikachu.attach_energy("Lightning")
result = game2.execute_attack(fresh_pikachu, thunder_shock, geodude, game2.opponent_board, game2.player_board)
print("Attack succeeded?", result)
print("Geodude damage taken:", geodude.damage_taken)
print("Geodude current HP:", geodude.current_hp())

# Test 3: Weakness match - double damage, should KO and award prize
print("\n--- Test 3: Attack that triggers weakness and KO ---")
fresh_squirtle.attach_energy("Colorless")
result = game2.execute_attack(fresh_squirtle, tackle, geodude, game2.opponent_board, game2.player_board)
print("Attack succeeded?", result)
print("Geodude damage taken:", geodude.damage_taken)
print("Is Geodude knocked out?", geodude.is_knocked_out())

print("\nOpponent's active after KO:", game2.opponent_board.active)
print("Opponent's discard pile:", [p.name for p in game2.opponent_board.discard_pile])
print("Player prizes remaining (after KO):", game2.player_board.prizes_remaining)
print("Opponent prizes remaining (unchanged):", game2.opponent_board.prizes_remaining)

# ============================================
# RETREAT TESTS
# ============================================
print("\n\n=== RETREAT TESTS ===")

retreat_board = Board()

active_pikachu = Pokemon("Pikachu", 60, "Lightning", "Fighting", [thunder_shock], 1)
bench_squirtle = Pokemon("Squirtle", 50, "Water", "Lightning", [tackle], 1)
bench_bulbasaur = Pokemon("Bulbasaur", 50, "Grass", "Fire", [tackle], 1)

retreat_board.set_active(active_pikachu)
retreat_board.add_to_bench(bench_squirtle)
retreat_board.add_to_bench(bench_bulbasaur)

print("Active before retreat:", retreat_board.active.name)
print("Bench before retreat:", [p.name for p in retreat_board.bench])

# Test 1: Try retreat with NOT enough energy (Pikachu has 0 energy, needs 1)
print("\n--- Test 1: Retreat without enough energy ---")
result1 = retreat_board.retreat(0)
print("Retreat successful?", result1)
print("Active (should be unchanged):", retreat_board.active.name)
print("Bench (should be unchanged):", [p.name for p in retreat_board.bench])

# Test 2: Attach energy, then retreat successfully
print("\n--- Test 2: Retreat with enough energy ---")
active_pikachu.attach_energy("Lightning")
print("Pikachu energy attached:", active_pikachu.energy_attached)

result2 = retreat_board.retreat(0)
print("Retreat successful?", result2)
print("Active after retreat:", retreat_board.active.name)
print("Bench after retreat:", [p.name for p in retreat_board.bench])
print("Pikachu energy after retreat (should be empty):", active_pikachu.energy_attached)

# Test 3: Try retreat with invalid bench index
print("\n--- Test 3: Retreat with invalid bench index ---")
result3 = retreat_board.retreat(10)
print("Retreat successful? (should be False)", result3)