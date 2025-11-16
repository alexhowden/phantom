import pyautogui as pag
from config import CONFIG
import mss
from core.state import PHANTOM
import numpy as np
from ultralytics import YOLO
import time
import sys

RESET = "\033[0m"
CYAN = "\033[96m"

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
            print(CYAN + line[:i] + RESET)
        time.sleep(0.016)
    print("\n\033[95mPhantom Bot is ready.\033[0m\n")

def capture_screen(mntr: dict):
	'''Capture the game window using mss and return it as a numpy array to be used in a model call'''
	with mss.mss() as sct:
		monitor = {
			'top': mntr[0],
			'left': mntr[1],
			'width': mntr[2],
			'height': mntr[3]
		}

		sct_img = sct.grab(monitor)

		# save image for debugging
		# output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
		# mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

		np_img = np.array(sct_img)
		img = np_img[:, :, :3]

		return img

def pixel_matches(img, x, y, target_rgb, tolerance=15):
	'''
	Check if the pixel at (x, y) matches the target RGB color within a tolerance.
	'''
	b, g, r = img[y, x]
	pixel_rgb = (r, g, b)
	# DEBUGGING
	# print(f'rgb: {pixel_rgb}')
	diff = np.linalg.norm(np.array(pixel_rgb) - np.array(target_rgb))
	return diff <= tolerance

def check_storages():
	print(f'Checking storages...')

	validate_state(desired_state='home', err_msg='can\'t check storages.')

	gold_full = pixel_matches(img=capture_screen(CONFIG.coords.gold_storage_dimensions), x=0, y=0, target_rgb=(239, 215, 119))

	elixir_full = pixel_matches(img=capture_screen(CONFIG.coords.elixir_storage_dimensions), x=0, y=0, target_rgb=(214, 149, 223))

	if gold_full and elixir_full:
		print(f'Gold is full. Upgrading walls.\n')
		upgrade_walls(resource='gold')
		print(f'Elixir is full. Upgrading walls.\n')
		upgrade_walls(resource='elixir')
	else:
		print(f'At least one storage not full.\n')

def get_state():
	'''Get the current state of phantom using the yolo model to detect which buttons are currently on the screen'''

	# DEBUGGING
	print('Fetching current state...')

	model = YOLO('models/yolo11s_state.pt')
	results = model.predict(source=capture_screen(CONFIG.coords.state_window_dimensions), verbose=False, conf=0.8, show=False)[0]
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
	time.sleep(0.1)
	pag.click(CONFIG.coords.confirm_surrender_button)
	time.sleep(0.5)

def val_end_battle():
	pag.click(CONFIG.coords.end_battle_button)
	time.sleep(1.5)

def val_return_home():
	pag.click(CONFIG.coords.return_home_button)
	time.sleep(1.5)

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
		time.sleep(1)
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

def upgrade_walls(resource: str):
	pag.click(CONFIG.coords.builder_button)
	time.sleep(0.1)

	for i in range(2):
		pag.moveTo(500, 930)
		pag.drag(0, -210, duration=2, button='left')
		time.sleep(0.5)

	pag.click(430, 870)
	time.sleep(0.25)

	for i in range(5):
		pag.click(480, 1010)

	if resource == 'gold':
		pag.click(550, 1010)
	else:
		pag.click(625, 1010)

	time.sleep(0.2)
	pag.click(555, 940)
	time.sleep(0.2)
