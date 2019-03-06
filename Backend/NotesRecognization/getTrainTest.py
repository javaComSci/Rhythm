import os
import numpy as np
import cv2
from PIL import Image
import re
import imageio
import random
from random import shuffle

# split the data into training and testing
def splitData(symbols):

	translations = {}
	trainingIn = np.empty((1, 3500))
	trainingOut = np.empty((1, 1))
	testingIn = np.empty((1, 3500))
	testingOut = np.empty((1, 1))
	count = 0

	for symbol in symbols.keys():

		symbolName = re.split('/', symbol)[2]
		print("SYMBOL", symbols[symbol].shape)
		translations[count] = symbolName

		trainingIn = np.vstack((trainingIn, symbols[symbol][1:400]))

		currTrainingOut = np.array(np.ones(399) * count).reshape((399, 1))
		trainingOut = np.vstack((trainingOut, currTrainingOut))

		testingIn = np.vstack((testingIn, symbols[symbol][400:]))

		currTestingOut = np.array((np.ones(len(symbols[symbol])-400) * count)).reshape(len(symbols[symbol])-400, 1)
		testingOut = np.vstack((testingOut, currTestingOut))

		count += 1

	# array delete first row
	trainingIn = np.delete(trainingIn, 0, 0)
	testingIn = np.delete(testingIn, 0, 0)
	trainingOut = np.delete(trainingOut, 0, 0)
	testingOut = np.delete(testingOut, 0, 0)

	print("TRANSLATIONS", translations)

	# scale the values
	trainingIn = trainingIn/255
	testingIn = testingIn/255

	print("TRAINING", trainingIn, " TRAINING", trainingOut, " TESTING", testingIn, " TESTING", testingOut, translations)
	print(trainingIn.shape, trainingOut.shape, testingIn.shape, testingOut.shape)
	return trainingIn, trainingOut, testingIn, testingOut, translations

# modify the image to have horizontal lines through them
def modifyImg(pixelArr):
	# choose one of the rows and see if it has black pixels, if yes, then add horizontal line through, else call again
	randRow = random.randint(0, pixelArr.shape[0]-1)

	# find the first occurence of black pixel
	minPixelInd = np.nanargmin(pixelArr[randRow])
	minPixel = pixelArr[randRow][minPixelInd]

	# didn't pick a row with a black pixel
	if minPixel != 0:
		return modifyImg(pixelArr)

	# from 0 to 50 the number of columns
	startInd = random.randint(0, pixelArr.shape[1] - 1)
	endInd = random.randint(startInd, pixelArr.shape[1] - 1)

	for i in range(startInd, endInd):
		pixelArr[randRow][i] = 0

	return pixelArr

# will go though the dataset to separate the data into training and testing sets
def getTrainingAndTestingData():
	symbols = {}
	symbolsDir = './SymbolsDatasetParsedSmall'
	modImageCount = 0
	# data has already been parsed into images, need to group and change into pixels for training
	for (dirName, subdirList, files) in os.walk(symbolsDir):
		if dirName == './SymbolsDatasetParsedSmall':
			continue

		# all in specific directory are of specific type
		symbols[dirName] = np.empty((1, 3500))

		# randomly shuffle the files in the folder
		shuffle(files)

		for file in files:
			# make sure that it is not a hidden file
			if file[0] == '.':
				continue

			# parse file path
			filePath = os.path.join(dirName, file)

			# repixel for the size
			pixelArr = Image.open(filePath)
			pixelArr = pixelArr.convert('L')
			pixelArr = pixelArr.resize((50, 70))
			pixelArr = np.array(pixelArr)
			img = Image.fromarray(pixelArr)
			# img.show()
			# return


			# randomly set approximately 10% of the images to have lines through them

			randInt = random.randint(0, 10)
			if randInt == 5:
				pixelArr = modifyImg(pixelArr)

				modImageCount += 1

				# just save the images with lines in them
				img = Image.fromarray(pixelArr)
				pathName = './ModifiedSymbols/' + str(modImageCount) + '.png'
				img.save(pathName)

				# for displaying the image
				# img = Image.fromarray(pixelArr)
				# img.show()
				# return

			# print("SHAPE IS ", pixelArr, pixelArr.shape)

			# flatten numpy array and reshape
			pixelArrFlat = pixelArr.flatten()
			pixelArrFlat = pixelArrFlat.reshape(pixelArrFlat.shape[0], 1).T

			# for each of the symbols, there is an array of dimension (401, 3500) with 401 samples
			symbols[dirName] = np.append(symbols[dirName], pixelArrFlat, axis = 0)
		print("SYMBOLS", dirName, symbols[dirName], symbols[dirName].shape, symbols[dirName][0].shape)
	trainingIn, trainingOut, testingIn, testingOut, translations = splitData(symbols)

	# write data to file
	# np.save('trainingIn.npy', trainingIn)
	# np.save('trainingOut.npy', trainingOut)
	# np.save('testingIn.npy', testingIn)
	# np.save('testingOut.npy', testingOut)
	# np.save('translations.npy', translations)


	np.save('trainingInWithLines.npy', trainingIn)
	np.save('trainingOutWithLines.npy', trainingOut)
	np.save('testingInWithLines.npy', testingIn)
	np.save('testingOutWithLines.npy', testingOut)
	np.save('translationsWithLines.npy', translations)

if __name__ == '__main__':
	getTrainingAndTestingData()