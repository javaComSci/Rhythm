import tensorflow as tf
import numpy as np

# get the data from where it was stored
def getData():
	trainingIn = np.load('trainingIn.npy')
	trainingOut = np.load('trainingOut.npy')
	testingIn = np.load('testingIn.npy')
	testingOut = np.load('testingOut.npy')

	return trainingIn, trainingOut, testingIn, testingOut
	
def trainNN(trainingIn, trainingOut, testingIn, testingOut):
	pass

	return trainingIn, trainingOut, testingIn, testingOut
if __name__ == '__main__':
	trainingIn, trainingOut, testingIn, testingOut = getData()
	trainNN(trainingIn, trainingOut, testingIn, testingOut)
