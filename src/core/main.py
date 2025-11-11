from config.valid_points import pick_random_point
import pyautogui as pag
from config import CONFIG
import yaml
import random
import mss
from core.state import PHANTOM
import numpy as np
from ultralytics import YOLO
import time

def run():
	output = pick_random_point('ldplayer')

run()

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
	model = YOLO('models/yolo11s_state.pt')
	results = model.predict(source=capture_screen(), conf=0.8, show=False)[0]
	time.sleep(2)
	buttons = [model.names[int(c)] for c in results.boxes.cls]

	if 'attack_button' in buttons:
		state = 'home'
	elif 'next_button' in buttons:
		state = 'search'
	elif 'end_battle' in buttons or 'surrender_button' in buttons:
		state = 'attack'
	elif 'surrender_button' in buttons:
		state = 'post'
	else:
		state = 'unknown'

	PHANTOM.update_state(state)
	return state

get_state()

def start_search():
	if PHANTOM.current_state != 'home':
		print('not home, can\'t start attack')
		return None
	pag.doubleClick(
		CONFIG.coords.attack_button[0],
		CONFIG.coords.attack_button[1]
	)
	time.sleep(0.5)
	pag.click(
		CONFIG.coords.find_match_button[0],
		CONFIG.coords.find_match_button[1]
	)

def attack():
	pag

time.sleep(1)
start_search()
attack()
