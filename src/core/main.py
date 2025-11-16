from core.attack import ATTACKSTRATEGY
from core.bot import *


def run():
	ATTACKSTRATEGY.attack_sequence()
	check_storages()

	# upgrade_walls('gold')

if __name__ == '__main__':
	startup_banner()

	while True:
		run()
