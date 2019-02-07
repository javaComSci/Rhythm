import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.models import Sequential
import cv2
from PIL import Image
from keras.layers import Dense

translations = np.load('translations.npy')
translations = translations.item()
print("TRANLSATIONS", translations)

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

	# print("TRAINING IN")
	# for i in testingIn[0]:
		# print(i)

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
	# modify the labels for clefs, notes, and times for training data
	for t in range(0, len(trainingOut)):
		output = trainingOut[t][0]
		
		translation = translations[output]
		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			trainingOut[t][0] = 0
		elif translation == '4-4-Time' or translation == '2-2-Time':
			# for time
			trainingOut[t][0] = 1
		else:
			# for note
			trainingOut[t][0] = 2

	# modify the labels for clefs, notes, and times for testing data
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			testingOut[t][0] = 0
		elif translation == '4-4-Time' or translation == '2-2-Time':
			# for time
			testingOut[t][0] = 1
		else:
			# for note
			testingOut[t][0] = 2
	
	# create model sequential
	model = Sequential()

	# add layers to model - works well with 1 hidden layer with 50 as well
	model.add(Dense(50, input_dim=3500, activation='relu'))
	model.add(Dense(20, activation='relu'))
	model.add(Dense(3, activation='softmax'))

	# compile the model with optimizer
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	# train the model
	model.fit(trainingIn, trainingOut, epochs=20)

	# see how it does on test dataset
	testLoss, testAcc = model.evaluate(testingIn, testingOut)
	print('Test Accuracy', testAcc)

	# predictions on unseen data
	predictions = model.predict(testingIn)
	overallPredictions = -np.ones((len(testingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print(overallPredictions[i], testingOut[i])

		testing = trainingIn[4050]
		testing = testing * 255

		print("TESTING IN SIZE", testing, testing.shape)
		testing = testing.reshape(70, 50)
		print("TESTING IN", testing)
		img = Image.fromarray(testing)
		img.show()
		return

	print("PREDICTIONS", overallPredictions)

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
