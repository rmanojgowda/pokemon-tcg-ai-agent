class Board:
    def __init__(self):
        self.active = None
        self.bench = []
        self.prizes_remaining = 6
        self.discard_pile = []

    def set_active(self, pokemon):
        self.active = pokemon

    def add_to_bench(self, pokemon):
        if len(self.bench) < 5:
            self.bench.append(pokemon)
            return True
        return False

    def knock_out_active(self):
        self.discard_pile.append(self.active)
        self.active = None

    def promote_from_bench(self, index):
        if self.active is not None:
            return False
        if index < 0 or index >= len(self.bench):
            return False
        self.active = self.bench.pop(index)
        return True
    
    def retreat(self, bench_index):
        if self.active is None:
            return False
        if bench_index < 0 or bench_index >= len(self.bench):
            return False

        retreat_cost = self.active.retreat_cost
        if len(self.active.energy_attached) < retreat_cost:
            return False

        for _ in range(retreat_cost):
            self.active.energy_attached.pop()

        old_active = self.active
        new_active = self.bench.pop(bench_index)

        self.bench.append(old_active)
        self.active = new_active

        return True