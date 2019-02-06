import os
import numpy as np
import cv2
from PIL import Image
import re
import imageio

# split the data into training and testing
def splitData(symbols):

	translations = {}
	trainingIn = np.empty((1, 55296))
	trainingOut = np.empty((1, 1))
	testingIn = np.empty((1, 55296))
	testingOut = np.empty((1, 1))
	count = 0

	for symbol in symbols.keys():

		symbolName = re.split('/', symbol)[2]
		print("SYMBOL", symbols[symbol].shape)
		translations[count] = symbolName

		trainingIn = np.vstack((trainingIn, symbols[symbol][1:51]))

		currTrainingOut = np.array(np.ones(50) * count).reshape((50, 1))
		trainingOut = np.vstack((trainingOut, currTrainingOut))

		testingIn = np.vstack((testingIn, symbols[symbol][51:]))

		currTestingOut = np.array((np.ones(len(symbols[symbol])-51) * count)).reshape(len(symbols[symbol])-51, 1)
		testingOut = np.vstack((testingOut, currTestingOut))

		count += 1

	# array delete first row
	trainingIn = np.delete(trainingIn, 0, 1)
	testingIn = np.delete(testingIn, 0, 1)
	trainingOut = np.delete(trainingOut, 0, 1)
	testingOut = np.delete(testingOut, 0, 1)

	print("TRANSLATIONS", translations)

	# scale the values
	trainingIn = trainingIn/255.0
	testingIn = testingIn/255.0

	print("TRAINING", trainingIn, " TRAINING", trainingOut, " TESTING", testingIn, " TESTING", testingOut, translations)
	print(trainingIn.shape, trainingOut.shape, testingIn.shape, testingOut.shape)
	return trainingIn, trainingOut, testingIn, testingOut, translations

# will go though the dataset to separate the data into training and testing sets
def getTrainingAndTestingData():
	symbols = {}
	symbolsDir = './SymbolsDatasetParsedMini'
	# data has already been parsed into images, need to group and change into pixels for training
	for (dirName, subdirList, files) in os.walk(symbolsDir):
		if dirName == './SymbolsDatasetParsedMini':
			continue

		# all in specific directory are of specific type
		symbols[dirName] = np.empty((1, 55296))

		for file in files:
			# make sure that it is not a hidden file
			if file[0] == '.':
				continue

			# parse file path
			filePath = os.path.join(dirName, file)

			# change png to numpy array
			pixelArr = imageio.imread(filePath)

			# for displaying the image
			# img = Image.fromarray(pixelArr, 'RGB')
			# img.show()

			# flatten numpy array and reshape
			pixelArrFlat = pixelArr.flatten()
			pixelArrFlat = pixelArrFlat.reshape(pixelArrFlat.shape[0], 1).T

			# for each of the symbols, there is an array of dimension (401, 55296) with 401 samples
			symbols[dirName] = np.append(symbols[dirName], pixelArrFlat, axis = 0)
		print("SYMBOLS", dirName, symbols[dirName], symbols[dirName].shape, symbols[dirName][0].shape)
	trainingIn, trainingOut, testingIn, testingOut, translations = splitData(symbols)

if __name__ == '__main__':
	getTrainingAndTestingData()