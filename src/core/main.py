from config.valid_points import pick_random_point
import pyautogui as pag
from config import CONFIG
from core.state import PHANTOM
from core.attack import ATTACKSTRATEGY
import time
from core.bot import *
import sys


def run():
	startup_banner()

	start_search()

	ATTACKSTRATEGY.attack()

	i = 0

	while True:
		print(i)
		time.sleep(1)
		i += 1



if __name__ == '__main__':
	run()

'''
20s
10s
25s
'''
