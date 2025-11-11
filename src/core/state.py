class PhantomState:
	def __init__(self):
		self.current_state = 'unknown'
		self.troop_cap = 320
		self.heroes_available = 4
		self.attack_strategy = 'barbarian_blitz'
		self.cooldowns = {}
		self.error_count = 0

	def update_state(self, state: str):
		self.current_state = state


PHANTOM = PhantomState()
