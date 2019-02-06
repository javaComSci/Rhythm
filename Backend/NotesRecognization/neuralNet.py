import tensorflow as tf
from tensorflow import keras
import numpy as np

# SYMBOL TABLE
	# - clef
	# 	- G
	# 	- C
	# 	- F
	# - note
	# 	- real note
	# 		- eighth
	# 		- half
	# 		- quarter
	# 		- whole
	# 	- rest
	# 		- eighth rest
	# 		- quarter rest
	# 		- whole-half rest
	# 	- extra
	# 		- sharp
	# 		- flat
	# - time
	# 	- 4 4
	# 	- 2 2 

# get the data from where it was stored
def getData():
	trainingIn = np.load('trainingIn.npy')
	trainingOut = np.load('trainingOut.npy')
	testingIn = np.load('testingIn.npy')
	testingOut = np.load('testingOut.npy')

	return trainingIn, trainingOut, testingIn, testingOut

def trainClefNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainNoteNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainTimeNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainExtraNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainRestNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut):
	model = keras.Sequential()

def predictClef(symbol):
	# which clef
	return

def predictRest(symbol):
	return

def predictExtra(symbol):
	return

def predictRealNote(symbol):
	return

def predictNote(symbol):
	# what type of note
	res = None
	
	if res == 'realNote':
		return predictRealNote(symbol)
	if res == 'rest':
		return predictRest(symbol)
	elif res == 'extra':
		return predictExtra(symbol)

def predictTime(symbol):
	# time
	return

def predict(symbol):
	res = None

	# general classes - clef, note, or time
	if res == 'clef':
		return predictClef(symbol)
	elif res == 'note':
		return predictNote(symbol)
	elif res == 'time':
		return predictTime(symbol)


if __name__ == '__main__':
	trainingIn, trainingOut, testingIn, testingOut = getData()
	trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut)
