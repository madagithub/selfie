import cv2
import numpy as np
import imutils

import pygame
from pygame.locals import *

WAITING_FOR_START = 0
WAITING_FOR_PHOTO_1 = 1
WAITING_FOR_PHOTO_2 = 2
SUMMARY = 3

pygame.init()
pygame.mouse.set_visible(False)

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

state = WAITING_FOR_START

language = None
image1 = None
image2 = None

sounds = { 
	'en': ['assets/H1.ogg', 'assets/H2.ogg', 'assets/H3.ogg'],
	'he': ['assets/H1.ogg', 'assets/H2.ogg', 'assets/H3.ogg'],
	'ar': ['assets/H1.ogg', 'assets/H2.ogg', 'assets/H3.ogg']
}

def soundDone():
	global state, image1, image2

	if state == WAITING_FOR_PHOTO_1:
		# Take picture
		ret, image1 = camera1.read()
		image1 = getSurfaceFromFrame(imutils.rotate_bound(image1, 90))

		# Play next sound
		pygame.mixer.music.load(sounds[language][1])
		pygame.mixer.music.play()
		state = WAITING_FOR_PHOTO_2
	elif state == WAITING_FOR_PHOTO_2:
		# Take picture
		ret, image2 = camera2.read()
		image2 = getSurfaceFromFrame(imutils.rotate_bound(image2, 90))

		# Play summary sound
		pygame.mixer.music.load(sounds[language][2])
		pygame.mixer.music.play()
		state = SUMMARY

def getSurfaceFromFrame(frame):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = np.fliplr(frame)
	frame = np.rot90(frame)
	return pygame.surfarray.make_surface(frame)

def startGame():
	global state

	state = WAITING_FOR_PHOTO_1
	isGameRunning = False
	pygame.mixer.music.load(sounds[language][0])
	pygame.mixer.music.play()

isGameRunning = True
clock = pygame.time.Clock()

while isGameRunning:
	screen.fill([0,0,0])

	if state == SUMMARY:
		spaceX = (screen.get_width() - 2 * image1.get_width()) // 3
		spaceY = (screen.get_height() - image1.get_height()) // 2
		screen.blit(image1, (spaceX, spaceY))
		screen.blit(image2, (spaceX * 2 + image1.get_width(), spaceY))
	elif state == WAITING_FOR_PHOTO_1 or state == WAITING_FOR_PHOTO_2:
		if not pygame.mixer.music.get_busy():
			soundDone()

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_e:
				language = 'en'
				startGame()
			elif event.key == K_h:
				language = 'he'
				startGame()
			elif event.key == K_a:
				language = 'ar'
				startGame()
			elif event.key == K_q:
				isGameRunning = False

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
cv2.destroyAllWindows()