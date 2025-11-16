from config.valid_points import pick_random_point
import pyautogui as pag
from config import CONFIG
import time
import sys
from core.bot import validate_state

class AttackStrategy:
	def __init__(self):
		self.strategies = ['super_barbs']
		self.current_strategy = 'super_barbs'

	def update_strategy(self, strategy: str):
		if strategy not in self.strategies:
			print(f'Invalid attack {strategy}.\n Terminating Phantom.\n')
			sys.exit(1)

		self.current_strategy = strategy

	def surrender(self):
		validate_state(desired_state='attack', err_msg='can\'t surrender.')

		pag.click(CONFIG.coords.surrender_button)
		time.sleep(0.1)
		pag.click(CONFIG.coords.confirm_surrender_button)
		time.sleep(0.5)

	def end_battle(self):
		validate_state(desired_state='search', err_msg='can\'t end battle.')

		pag.click(CONFIG.coords.end_battle_button)
		time.sleep(1.5)

	def return_home(self):
		validate_state(desired_state='post', err_msg='can\'t return home.')

		pag.click(CONFIG.coords.return_home_button)
		time.sleep(1.5)

	def search(self):
		validate_state(desired_state='home', err_msg='can\'t search for base.')

		print('Searching for base\n')

		pag.doubleClick(CONFIG.coords.attack_button)
		time.sleep(0.5)
		pag.click(CONFIG.coords.find_match_button)
		time.sleep(3)

	def attack(self):
		validate_state(desired_state='search', err_msg='can\'t start attack.')

		print('Attacking base\n')

		match self.current_strategy:
			case 'super_barbs':
				self.attack_super_barbs()

	def attack_sequence(self):
		self.search()
		self.attack()
		self.surrender()
		self.return_home()

	def attack_super_barbs(self):
		# select super barbs
		pag.click(CONFIG.coords.super_barbs_button)

		# start battle to get rid of buttons
		pag.click(CONFIG.coords.base_right_corner)

		# deploy remaining barbarians
		print('Deploying super barbarians...')
		points = pick_random_point('ldplayer', n=32)
		for point in points:
			pag.doubleClick(point)

		# use eq and lightning
		print('Deploying spells...')
		pag.click(CONFIG.coords.earthquake_button)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)

		pag.click(CONFIG.coords.lightning_button)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)
		pag.doubleClick(
			(CONFIG.coords.right + CONFIG.coords.left) / 2 + 50,
			(CONFIG.coords.bottom + CONFIG.coords.top) / 2
		)

		print('Deploying siege machine and heroes...')
		# move to the bottom of the base
		pag.click(480, 1025)
		pag.drag(xOffset=0, yOffset=-250, duration=0.25, button='left')

		# deploy siege machine
		pag.click(CONFIG.coords.siege_machine_button)
		pag.click(CONFIG.coords.base_bottom_corner)

		# deploy heroes
		heroes = [
			CONFIG.coords.barbarian_king_button,
			CONFIG.coords.archer_queen_button,
			CONFIG.coords.grand_warden_button,
			CONFIG.coords.royal_champion_button
		]

		for hero in heroes:
			pag.click(hero)
			pag.click(CONFIG.coords.base_bottom_corner)

		time.sleep(3)

		for hero in heroes:
			pag.click(hero)

		print('Waiting 20...')
		time.sleep(5)
		print('Waiting 15...')
		time.sleep(5)
		print('Waiting 10...')
		time.sleep(5)
		print('Waiting 5...\n')
		time.sleep(5)



ATTACKSTRATEGY = AttackStrategy()
