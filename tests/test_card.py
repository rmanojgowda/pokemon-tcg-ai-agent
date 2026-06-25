from tcg_engine.card import Pokemon, Attack
from tcg_engine.board import Board

# Create an attack
thunder_shock = Attack("Thunder shock", 30, ["Lightning", "Lightning"])
tackle = Attack("Tackle", 20, ["Colorless"])

# Create a Pokemon with attack
pikachu = Pokemon("Pikachu", 60, "Lightning", "Fighting", [thunder_shock], 1)
squirtle = Pokemon("Squirtle", 50, "Water", "Lightning", [tackle], 1)
bulbasaur = Pokemon("Bulbasaur", 50, "Grass", "Fire", [tackle], 1)


board = Board()
board.set_active(pikachu)
board.add_to_bench(squirtle)
board.add_to_bench(bulbasaur)

print("Active : ", board.active.name)
print("Bench : ", [p.name for p in board.bench])
print("Prizes remaining : ", board.prizes_remaining)

# Simulate pikachu knocked out
board.knock_out_active()
print("\nAfter knocking out :")
print("Active : ", board.active)
print("Discard pile : ", [p.name for p in board.discard_pile])

# Promote squirtle to bench
result = board.promote_from_bench(0)
print("\nPromotion succesful ? ", result)
print("Active :", board.active.name)
print("Bench : ", [p.name for p in board.bench])

# Test current_hp
print("Cuurnet Hp :", pikachu.current_hp())

# Test damage
pikachu.damage_taken = 20
print("After 20 damage, HP :", pikachu.current_hp())

#Test knocked out check
print("Is knocked out ?", pikachu.is_knocked_out())

#Test attack usability
print("Can use thunder shock with no energy", thunder_shock.can_use([]))
print("Can use thunder shock with 1 energy", thunder_shock.can_use(["Lightning"]))
print("Can use thunder shock with 2 energy", thunder_shock.can_use(["Lightning", "Lightning"]))
