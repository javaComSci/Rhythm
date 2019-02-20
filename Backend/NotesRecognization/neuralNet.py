import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.models import Sequential
import cv2
from PIL import Image
from keras.layers import Dense, Dropout
from keras.models import load_model
import math
import os
from clefNeuralNet import predictClef
os.environ['KMP_DUPLICATE_LIB_OK']='True'

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
	# data without lines
	# trainingIn = np.load('trainingIn.npy')
	# trainingOut = np.load('trainingOut.npy')
	# testingIn = np.load('testingIn.npy')
	# testingOut = np.load('testingOut.npy')

	# data with lines
	trainingIn = np.load('trainingInWithLines.npy')
	trainingOut = np.load('trainingOutWithLines.npy')
	testingIn = np.load('testingInWithLines.npy')
	testingOut = np.load('testingOutWithLines.npy')

	# print("TRAINING IN")
	# for i in testingIn[0]:
		# print(i)

	return trainingIn, trainingOut, testingIn, testingOut

def trainClefNN(trainingIn, trainingOut, testingIn, testingOut):

	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	cclefIndiciesTraining = np.where(trainingOut == 1)[0]
	gclefIndiciesTraining = np.where(trainingOut == 6)[0]
	fclefIndiciesTraining = np.where(trainingOut == 8)[0]

	# for inputs
	clefTrainingIn = trainingIn[cclefIndiciesTraining]
	clefTrainingIn = np.vstack((clefTrainingIn, trainingIn[gclefIndiciesTraining]))
	clefTrainingIn = np.vstack((clefTrainingIn, trainingIn[fclefIndiciesTraining]))

	# for outputs
	clefTrainingOut = trainingOut[cclefIndiciesTraining,:]
	clefTrainingOut = np.vstack((clefTrainingOut, trainingOut[gclefIndiciesTraining,:]))
	clefTrainingOut = np.vstack((clefTrainingOut, trainingOut[fclefIndiciesTraining,:]))

	# changing values
	clefTrainingOut[clefTrainingOut == 1] = 0
	clefTrainingOut[clefTrainingOut == 6] = 1
	clefTrainingOut[clefTrainingOut == 8] = 2


	#TESTING DATA CLEANING
	# row indicies
	cclefIndiciesTesting = np.where(testingOut == 1)[0]
	gclefIndiciesTesting = np.where(testingOut == 6)[0]
	fclefIndiciesTesting = np.where(testingOut == 8)[0]

	# for inputs
	clefTestingIn = testingIn[cclefIndiciesTesting]
	clefTestingIn = np.vstack((clefTestingIn, testingIn[gclefIndiciesTesting]))
	clefTestingIn = np.vstack((clefTestingIn, testingIn[fclefIndiciesTesting]))

	# for outputs
	clefTestingOut = testingOut[cclefIndiciesTesting,:]
	clefTestingOut = np.vstack((clefTestingOut, testingOut[gclefIndiciesTesting,:]))
	clefTestingOut = np.vstack((clefTestingOut, testingOut[fclefIndiciesTesting,:]))

	# changing values
	clefTestingOut[clefTestingOut == 1] = 0
	clefTestingOut[clefTestingOut == 6] = 1
	clefTestingOut[clefTestingOut == 8] = 2

	# testing = clefTrainingIn[370]
	# testing = testing * 255
	# testing = testing.reshape(70, 50)
	# img = Image.fromarray(testing)
	# img.show()
	# return

	# print("TRAINING", cclefIndiciesTraining, gclefIndiciesTraining, fclefIndiciesTraining, clefTrainingIn, clefTrainingIn.shape, clefTrainingOut, clefTrainingOut.shape)
	# print("TESTING", clefTestingIn.shape, clefTestingIn, clefTestingOut, clefTestingOut.shape)

	print("SHAPES", clefTestingIn.shape, clefTestingOut.shape, clefTrainingIn.shape, clefTrainingOut.shape)

	
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [20, 'relu'], [15, 'tanh'], [3, 'softmax'] ],
	[ [25, 'relu'], [5, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	[ [50, 'relu'], [3, 'softmax'] ],
	]

	model = hyperparameterTuning(clefTrainingIn, clefTrainingOut, clefTestingIn, clefTestingOut, layersForTraining)

	model.save('clef_model.h5')

	model = load_model('clef_model.h5')

	# predictions on unseen data
	predictions = model.predict(testingIn)
	overallPredictions = -np.ones((len(testingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print(overallPredictions[i], testingOut[i])

		testing = trainingIn[1000]
		testing = testing * 255
		testing = testing.reshape(70, 50)
		img = Image.fromarray(testing)
		img.show()
		return

	print("PREDICTIONS", overallPredictions)


def trainNoteNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainTimeNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainExtraNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainRestNN(trainingIn, trainingOut, testingIn, testingOut):
	return

def trainModel(trainingIn, trainingOut, modelInfo):
	# create model sequential
	model = Sequential()

	# add first layer
	model.add(Dense(modelInfo[0][0], input_dim=3500, activation=modelInfo[0][1]))

	# each layer is given activation function and number of neurons
	for i in range(1, len(modelInfo)):
		model.add(Dense(modelInfo[i][0], activation=modelInfo[i][1]))

	# compile the model with optimizer
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	model.summary()

	# train the model
	model.fit(trainingIn, trainingOut, epochs=20)

	return model

def hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, modelsInfo):
	# modelInfo is an array of models with layer info for each model
	# layers info is in form of [[[numNeurons,activationFunction],....]], 
	# stores the best model after hyperparamter tuning
	bestModel = None
	bestTestAcc = -math.inf
	allModels = {}

	modelCount = 0
	# go through all models to be trained with
	for modelInfo in modelsInfo:
		
		model = trainModel(trainingIn, trainingOut, modelInfo)

		# see how it does on test dataset
		testLoss, testAcc = model.evaluate(testingIn, testingOut)
		print('Test Accuracy', testAcc)

		if testAcc > bestTestAcc:
			bestTestAcc = testAcc
			bestModel = model

		allModels[model] = testAcc

	for m in allModels.keys():
		print("MODEL: ", m, " ACCURACY: ", allModels[m])
	bestModel.summary()
	return bestModel

def trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut):

	print("TRANING INPUT", trainingOut.shape, trainingIn.shape)
	# return
	# modify the labels for clefs, notes, and times for training data
	for t in range(0, len(trainingOut)):
		output = trainingOut[t][0]
		
		translation = translations[output]
		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			trainingOut[t][0] = 0
		else:
			# for note
			trainingOut[t][0] = 1

	# modify the labels for clefs, notes, and times for testing data
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			testingOut[t][0] = 0
		else:
			# for note
			testingOut[t][0] = 1

	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [20, 'relu'], [15, 'tanh'], [3, 'softmax'] ],
	[ [50, 'relu'], [3, 'softmax'] ],
	[ [40, 'tanh'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	[ [300, 'relu'], [3, 'softmax'] ],
	]

	model = hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, layersForTraining)

	print("CALLING HYPERPARAMETER TUNING")

	model.save('general_model.h5')

	model = load_model('general_model.h5')

	# # predictions on unseen data
	# predictions = model.predict(testingIn)
	# overallPredictions = -np.ones((len(testingOut),1))

	# print("ALL THE PREDICTIONS", overallPredictions)

	# for i in range(predictions.shape[0]):
	# 	overallPredictions[i] = np.argmax(predictions[i])
	# 	print(overallPredictions[i], testingOut[i])

	# 	testing = trainingIn[1000]
	# 	testing = testing * 255

	# 	print("TESTING IN SIZE", testing, testing.shape)
	# 	testing = testing.reshape(70, 50)
	# 	print("TESTING IN", testing)
	# 	img = Image.fromarray(testing)
	# 	img.show()
	# 	return

	# print("PREDICTIONS", overallPredictions)


def predictRest(symbol):
	return

def predictExtra(symbol):
	return

def predictRealNote(testingInput):
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

def checkPredictions(testingInput, testingOut):
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		translation = translations[output]

		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			testingOut[t][0] = 0
		else:
			# for note
			testingOut[t][0] = 1

	generalPredictions, clefPredictions = predict(testingInput)

	incorrectGeneral = 0
	correctGeneral = 0

	for i in range(generalPredictions.shape[0]):
		if generalPredictions[i] != testingOut[i]:
			incorrectGeneral += 1
		else:
			correctGeneral += 1

	incorrectClef = 0
	correctClef = 0

	for i in range(clefPredictions.shape[0]):
		if clefPredictions[i] != testingOut[i]:
			incorrectClef += 1
		else:
			correctClef += 1

	print("General incorrect", incorrectGeneral, "General Correct", correctGeneral)
	print("Clef incorrect", incorrectClef, "Clef Correct", correctClef)


def predict(testingIn):
	model = load_model('general_model.h5')

	# actual values for which one of the different types it could be
	generalPredictions = model.predict(testingIn)

	# actual value of the predictions
	overallPredictions = -np.ones((testingIn.shape[0],1))

	clefPredictions = []

	isclef = False

	for i in range(generalPredictions.shape[0]):
		overallPredictions[i] = np.argmax(generalPredictions[i])

		# send to respective neural network
		if overallPredictions[i] == 0:
			clefPrediction = predictClef(testingIn)
			clefPredictions.append(clefPrediction)
			isclef = True
			print("IT WAS A CLEF")
		else:
			notePrediction = predictNote(testingIn)

	# convert to numpy array
	# clefPredictions = np.asarray(clefPredictions)

	if isclef:
		print("OVERALL PREDICTION", overallPredictions[i], "THE CLEF PREDICTION IS ", clefPredictions[0])
		return clefPredictions[0]
	else:
		return overallPredictions[0]


		# testing = trainingIn[1000]
		# testing = testing * 255

		# print("TESTING IN SIZE", testing, testing.shape)
		# testing = testing.reshape(70, 50)
		# print("TESTING IN", testing)
		# img = Image.fromarray(testing)
		# img.show()
		# return

	# general classes - clef, note, or time
	# if res == 'clef':
	# 	return predictClef(symbol)
	# elif res == 'note':
	# 	return predictNote(symbol)


if __name__ == '__main__':

	trainingIn, trainingOut, testingIn, testingOut = getData()
	# trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut)
	# trainClefNN(trainingIn, trainingOut, testingIn, testingOut)
	checkPredictions(testingIn, testingOut)
