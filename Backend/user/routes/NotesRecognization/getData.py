import os
import numpy as np
import cv2
from PIL import Image
import re
import imageio


def getTrainingAndTestingData():
	symbols = {}
	symbolsDir = './SymbolsDatasetParsed'
	# data has already been parsed into images, need to group and change into pixels for training
	for (dirName, subdirList, files) in os.walk(symbolsDir):
		if dirName == './SymbolsDatasetParsed':
			continue

		# all in specific directory are of specific type
		symbols[dirName] = np.empty((55296, 1))

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

			# flatten numpy array
			pixelArrFlat = pixelArr.flatten()
			pixelArrFlat = pixelArrFlat.reshape(pixelArrFlat.shape[0], 1)

			symbols[dirName] = np.append(symbols[dirName], pixelArrFlat, axis = 1)
		print("SYMBOLS", dirName, symbols[dirName], symbols[dirName].shape)
	print("SYMBOLS", symbols)

if __name__ == '__main__':
	getTrainingAndTestingData()
