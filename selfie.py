import cv2
import numpy as np
import imutils

import pygame
from pygame.locals import *

from common.Timer import Timer

import datetime

MAX_CAPTURE_WIDTH = 1920
MAX_CAPTURE_HEIGHT = 1080

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MAX_DISPLAY_DIMS = (int(MAX_CAPTURE_HEIGHT * (SCREEN_HEIGHT / MAX_CAPTURE_WIDTH)), SCREEN_HEIGHT)

DELAY_BETWEEN_SOUNDS = 1
DELAY_UNTIL_PICTURES_SHOW = 0.3

WAITING_FOR_START = 0
WAITING_FOR_PHOTO = 1
SUMMARY = 2

pygame.init()
pygame.mouse.set_visible(False)

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(2)

camera1.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_CAPTURE_WIDTH);
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_CAPTURE_HEIGHT);

camera2.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_CAPTURE_WIDTH);
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_CAPTURE_HEIGHT);

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

state = WAITING_FOR_START

language = None
currImage1 = None
currImage2 = None
image1 = None
image2 = None
imageSurface1 = None
imageSurface2 = None

timer = None

cameraEffect = pygame.mixer.Sound('assets/camera.ogg')

sounds = {
	'en': ['assets/E1.ogg', 'assets/E2.ogg'],
	'he': ['assets/H1.ogg', 'assets/H2.ogg'],
	'ar': ['assets/A1.ogg', 'assets/A2.ogg']
}

def moveNext():
	global timer, state

	timer = None

	if state == WAITING_FOR_PHOTO:
		# Play second sound
		pygame.mixer.music.load(sounds[language][1])
		pygame.mixer.music.play()
		state = SUMMARY

def showPictures():
	global image1, image2, imageSurface1, imageSurface2, timer

	imageSurface1 = getSurfaceFromFrame(image1)
	imageSurface2 = getSurfaceFromFrame(image2)

	# Save both images with timestamp
	timeString = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	image = np.concatenate((image1, image2), axis=1)
	cv2.imwrite('images/' + timeString + '-image.png', image)

	timer = Timer(DELAY_BETWEEN_SOUNDS, moveNext)

def soundDone():
	global state, image1, image2, imageSurface1, imageSurface2, timer, camera1, camera2

	if state == WAITING_FOR_PHOTO:
		# Take pictures
		image1 = imutils.rotate_bound(currImage1.copy(), 270)
		image2 = imutils.rotate_bound(currImage2.copy(), 270)
		cameraEffect.play()

		timer = Timer(DELAY_UNTIL_PICTURES_SHOW, showPictures)

def getSurfaceFromFrame(frame):
	if frame.shape[1] > MAX_DISPLAY_DIMS[0] or frame.shape[0] > MAX_DISPLAY_DIMS[1]:
		frame = cv2.resize(frame, MAX_DISPLAY_DIMS)

	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = np.fliplr(frame)
	frame = np.rot90(frame)
	return pygame.surfarray.make_surface(frame)

def startGame():
	global state, timer

	timer = None
	state = WAITING_FOR_PHOTO
	isGameRunning = False
	pygame.mixer.music.load(sounds[language][0])
	pygame.mixer.music.play()

isGameRunning = True
clock = pygame.time.Clock()

lastTime = pygame.time.get_ticks()

while isGameRunning:
	ret1, currImage1 = camera1.read()
	ret2, currImage2 = camera2.read()

	screen.fill([0,0,0])

	if imageSurface1 is not None and imageSurface2 is not None:
		firstSpaceX = (screen.get_width() // 2 - imageSurface1.get_width())
		firstSpaceY = (screen.get_height() - imageSurface1.get_height()) // 2
		screen.blit(imageSurface2, (firstSpaceX, firstSpaceY))

		secondSpaceY = (screen.get_height() - imageSurface2.get_height()) // 2
		screen.blit(imageSurface1, (firstSpaceX + imageSurface1.get_width(), secondSpaceY))

	currTime = pygame.time.get_ticks()
	dt = (currTime - lastTime) / 1000
	lastTime = currTime

	if timer is not None:
		timer.tick(dt)
	elif state == WAITING_FOR_PHOTO:
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
