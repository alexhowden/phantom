from config.valid_points import pick_random_point
import pyautogui as pag
from config import CONFIG
from core.state import PHANTOM
from core.attack import ATTACKSTRATEGY
import time
from core.bot import *
import sys


def run():
	start_search()

	ATTACKSTRATEGY.attack()

	ATTACKSTRATEGY.surrender()

	ATTACKSTRATEGY.return_home()


if __name__ == '__main__':
	startup_banner()

	while True:
		run()

'''
20s
10s
25s
25s
10s
'''
