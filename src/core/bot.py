from config.valid_points import pick_random_point
import pyautogui as pag
from config import CONFIG
import yaml
import mss
from core.state import PHANTOM
import numpy as np
from ultralytics import YOLO
import time
import sys
import random

# ANSI colors
RESET = "\033[0m"
CYAN = "\033[96m"  # bright cyan

BANNER = [
    r"██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗",
    r"██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║",
    r"██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║",
    r"██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║",
    r"██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║",
    r"╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝"
]

def startup_banner():
    max_length = max(len(line) for line in BANNER)
    for i in range(max_length + 1):
        sys.stdout.write("\033[H\033[J")  # clear screen
        for line in BANNER:
            # print up to i characters of the line
            print(CYAN + line[:i] + RESET)
        time.sleep(0.03)  # speed of reveal
    print("\n\033[95mPhantom Bot is ready.\033[0m\n")

def capture_screen():
	'''Capture the game window using mss and return it as a numpy array to be used in a model call'''
	with mss.mss() as sct:
		monitor = {
			'top': CONFIG.coords.top,
            'left': CONFIG.coords.left,
            'width': CONFIG.coords.width,
            'height': CONFIG.coords.height
		}
		sct_img = sct.grab(monitor)

		# save image for debugging
		# output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
		# mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

		np_img = np.array(sct_img)
		img = np_img[:, :, :3]

		return img

def get_state():
	'''Get the current state of phantom using the yolo model to detect which buttons are currently on the screen'''

	# DEBUGGING
	print('Fetching current state...')

	model = YOLO('models/yolo11s_state.pt')
	results = model.predict(source=capture_screen(), verbose=False, conf=0.8, show=False)[0]
	time.sleep(2)
	buttons = [model.names[int(c)] for c in results.boxes.cls]
	print(f'buttons: {buttons}')

	if 'attack_button' in buttons:
		state = 'home'
	elif 'next_button' in buttons:
		state = 'search'
	elif 'end_battle_button' in buttons or 'surrender_button' in buttons:
		state = 'attack'
	elif 'return_home_button' in buttons:
		state = 'post'
	else:
		state = 'unknown'

	PHANTOM.update_state(state)

	# DEBUGGING
	print(f'Current state: {state}\n')

	return state

def val_surrender():
	pag.click(CONFIG.coords.surrender_button)
	pag.click(CONFIG.coords.confirm_surrender_button)

def val_end_battle():
	pag.click(CONFIG.coords.end_battle_button)

def val_return_home():
	pag.click(CONFIG.coords.return_home_button)

def val_start_search():
	pag.doubleClick(CONFIG.coords.attack_button)
	time.sleep(0.5)

	pag.click(CONFIG.coords.find_match_button)
	time.sleep(3)

def validate_state(desired_state: str, err_msg: str):
	'''Checks if the bot is in the desired state'''

	print('Validating current state...')
	print(f'Desired state: {desired_state}')
	state = get_state()

	while state == 'unknown':
		PHANTOM.log_error(f'Currently in {state} state, {err_msg}')
		state = get_state()

	PHANTOM.we_chillin()

	if state == desired_state:
		return state

	if desired_state == 'home':
		while state == 'search':
			print(f'Currently in {state} state, attempting to return home.')
			val_return_home()
			time.sleep(2)
			state = get_state()
		while state == 'attack':
			print(f'Currently in {state} state, attempting to return home.')
			val_surrender()
			time.sleep(2)
			state = get_state()
		while state == 'post':
			print(f'Currently in {state} state, attempting to return home.')
			val_return_home()
			time.sleep(2)
			state = get_state()

	if desired_state == 'search':
		while state == 'home':
			val_start_search()
			time.sleep(3)
			state = get_state()
		while state == 'attack':
			val_end_battle()
			time.sleep(2)
			val_return_home()
			time.sleep(2)
			val_start_search()
			time.sleep(2)
			state = get_state()
		while state == 'post':
			val_return_home()
			time.sleep(2)
			val_start_search()
			time.sleep(2)
			state = get_state()

	return state

def start_search():
	validate_state(desired_state='home', err_msg='can\'t search for base.')

	print('Searching for base\n')

	pag.doubleClick(CONFIG.coords.attack_button)
	time.sleep(0.5)

	pag.click(CONFIG.coords.find_match_button)
	time.sleep(3)

