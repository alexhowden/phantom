import sys

class PhantomState:
	def __init__(self):
		self.current_state = 'unknown'
		self.troop_cap = 320
		self.heroes_available = 4
		self.attack_strategy = 'barbarian_blitz'
		self.cooldowns = {}
		self.error_count = 0

	def update_state(self, state: str):
		'''Update current state of the bot'''
		self.current_state = state

	def log_error(self, err_msg: str):
		self.error_count += 1
		print(f'Error: {err_msg}')
		if self.error_count < 3:
			print(f'Trying again...\n')
		else:
			print(f'Too many errors. Terminating Phantom.\n')
			sys.exit(1)

	def we_chillin(self):
		self.error_count = 0

	def pretty_print(self):
		print('================ PHANTOM STATE ================')
		print(f'Current State      : {self.current_state}')
		print(f'Troop Cap          : {self.troop_cap}')
		print(f'Heroes Available   : {self.heroes_available}')
		print(f'Attack Strategy    : {self.attack_strategy}')
		print(f'Error Count        : {self.error_count}')
		if self.cooldowns:
			print('Cooldowns:')
			for action, ts in self.cooldowns.items():
				import time
				remaining = max(0, ts - time.time())
				print(f'  {action}: {remaining:.1f}s remaining')
		print('===============================================')


PHANTOM = PhantomState()
