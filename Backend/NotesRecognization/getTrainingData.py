import numpy as np
import cv2
import random
from os import walk
import os.path


def generateNotes(imgPath, name):
	imgCount = 1
	# modify for lines
	for (dirpath, dirnames, filenames) in walk(imgPath):
		for file in filenames:

			# open the image with grayscale
			fileToOpen = os.path.join(imgPath, file)
			im_gray = cv2.imread(fileToOpen, cv2.IMREAD_GRAYSCALE)

			# ignore if not images
			if '.DS_Store' in fileToOpen:
				continue

			# update image to binary
			thresh = 127
			im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

			# number of images to generate per image for clefs
			if name == 'GClef' or name == 'FClef':
				numImages = 5
			elif '_noLines' in fileToOpen:
				numImages = 300
			elif name == 'CClef' and '__noLines' not in fileToOpen:
				numImages = 40
			elif name == 'CClef' and '__noLines' in fileToOpen:
				numImages = 200
			elif 'Sharp' in fileToOpen or 'Flat' in fileToOpen:
				numImages = 200
			elif 'Rest' in fileToOpen:
				numImages = 200
			else:
				print('HERE')
				numImages = 34

			for i in range(1, numImages + 1):

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
				imgName =  './PrintedNotesParsed' + '/'+ name + '/' + name + str(imgCount) + '.png'
				cv2.imwrite(imgName, img)
				imgCount += 1


if __name__ == '__main__':
	# generateNotes('./SymbolsUnparsed/treble', 'GClef')
	# generateNotes('./SymbolsUnparsed/bass', 'FClef')
	# generateNotes('./SymbolsUnparsed/alto', 'CClef')

	path = './SymbolsUnparsed'
	for (dirpath, dirnames, filenames) in walk(path):
		# note type for modification
		for dirname in dirnames:
			# create path name
			dirToOpen = os.path.join(path, dirname)

			generateNotes(dirToOpen, dirname)

