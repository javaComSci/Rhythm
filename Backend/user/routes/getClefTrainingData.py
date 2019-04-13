import numpy as np
import cv2
import random
from os import walk
import os.path


def modifyClef(imgPath, imgPathLines, clefName):
	imgCount = 1
	# modify for lines
	for (dirpath, dirnames, filenames) in walk(imgPathLines):
		for file in filenames:

			# open the image with grayscale
			fileToOpen = os.path.join(imgPathLines, file)
			im_gray = cv2.imread(fileToOpen, cv2.IMREAD_GRAYSCALE)

			# ignore if not images
			if '.DS_Store' in fileToOpen:
				continue

			# update image to binary
			thresh = 127
			im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

			# number of images to generate per image
			numImages = 5
			if '_noLines' in fileToOpen:
				numImages = 300
			if imgPathLines == 'alto' and '__noLines' not in fileToOpen:
				numImages = 40
			if imgPathLines == 'alto' and '__noLines' in fileToOpen:
				numImages = 200

			for i in range(1, numImages):

				# generate a random width and height - stretch or shrink
				width = random.randint(25, 49)
				height = random.randint(30, 70)

				# resize image with random size
				img = cv2.resize(im_bw, (width, height), interpolation = cv2.INTER_LINEAR)

				# add white space around image to make it 70 by 70
				verticalPadding = int((70 - height)/2)
				horizontalPadding = int((50 - width)/2)
				WHITE = [255, 255, 255]
				img = cv2.copyMakeBorder(img, verticalPadding, verticalPadding, horizontalPadding, horizontalPadding, cv2.BORDER_CONSTANT, value=WHITE)
				
				# write image to folder
				imgName =  './'+ clefName + '/' + clefName + str(imgCount) + '.png'
				cv2.imwrite(imgName, img)
				imgCount += 1


if __name__ == '__main__':
	# modifyClef('GClef.png', 'treble', 'GClef')
	# modifyClef('FClef.png', 'bass', 'FClef')
	modifyClef('CClef.png', 'alto', 'CClef')