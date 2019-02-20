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


# load all translations
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


# @return - 2d numpy arrays with training and testing data 
# Loads the data from the numpy files
def getData():
	# data with lines
	trainingIn = np.load('trainingInWithLines.npy')
	trainingOut = np.load('trainingOutWithLines.npy')
	testingIn = np.load('testingInWithLines.npy')
	testingOut = np.load('testingOutWithLines.npy')

	# print("TRAINING IN")
	# for i in testingIn[0]:
		# print(i)

	return trainingIn, trainingOut, testingIn, testingOut



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with identifying the different clefs
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
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [20, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [25, 'relu'], [5, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	[ [10, 'relu'], [3, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(clefTrainingIn, clefTrainingOut, clefTestingIn, clefTestingOut, layersForTraining)

	# save the model for later use
	model.save('clef_model.h5')



# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network trained with clefs
def testClefNN(testingIn, testingOut):
	model = load_model('clef_model.h5')

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

	# predictions on unseen data
	predictions = model.predict(clefTestingIn)
	overallPredictions = -np.ones((len(clefTestingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", clefTestingOut[i])

		# showing the incorrect image
		# if overallPredictions[i] != clefTestingOut[i]:
		# 	testing = clefTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		# if i % 99 == 0:
		# 	testing = clefTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
			

	print("Accuracy on clef testing data:", (np.sum(overallPredictions == clefTestingOut)+0.0)/len(clefTestingOut))


# @TODO
# neural network for specific notes
def trainNoteNN(trainingIn, trainingOut, testingIn, testingOut):
	return



# @TODO
# neural network for different rests
def trainRestNN(trainingIn, trainingOut, testingIn, testingOut):
	return



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @modelIfo - array of models with layer info for each model of form [[[numNeurons,activationFunction],....]]
# @return - neural network model
# Add layers to sequential model, compile model, and fit the model
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



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @modelIfo - array of models with layer info for each model of form [[[numNeurons,activationFunction],....]]
# @return - neural network model
# Do hyperparameter tuning to find the best hyperparameters for a model
def hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, modelsInfo):
	# stores the best model after hyperparamter tuning
	bestModel = None
	bestTestAcc = -math.inf
	allModels = {}

	modelCount = 0
	# go through all models to be trained with
	for modelInfo in modelsInfo:
		
		# create and traing a model
		model = trainModel(trainingIn, trainingOut, modelInfo)

		# see how it does on test dataset
		testLoss, testAcc = model.evaluate(testingIn, testingOut)
		print('Test Accuracy', testAcc)

		# compare with the current best test accuracy
		if testAcc > bestTestAcc:
			bestTestAcc = testAcc
			bestModel = model

		allModels[model] = testAcc

	for m in allModels.keys():
		print("MODEL: ", m, " ACCURACY: ", allModels[m])
	bestModel.summary()
	return bestModel


# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Train the general neural network with training inputs and labels
def trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut):

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


	# create the layers that could be used for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [2, 'softmax'] ],
	[ [20, 'relu'], [15, 'tanh'], [2, 'softmax'] ],
	[ [50, 'relu'], [2, 'softmax'] ],
	[ [40, 'tanh'], [2, 'softmax'] ],
	[ [50, 'sigmoid'], [2, 'softmax'] ],
	[ [300, 'relu'], [2, 'softmax'] ],
	]

	# perform hyperparameter tuning
	model = hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, layersForTraining)

	# save the best model for the general NN
	model.save('general_model.h5')



# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network for the base
def testGeneralNN(testingIn, testingOut):
	model = load_model('general_model.h5')

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

	# predictions on unseen data
	predictions = model.predict(testingIn)
	overallPredictions = -np.ones((len(testingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", testingOut[i])

		# showing the incorrect image
		# if overallPredictions[i] != testingOut[i]:
		# 	testing = testingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		# if i % 100 == 0 and overallPredictions[i] == testingOut[i]:
		# 	testing = testingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()

	print("Accuracy on general testing data:", (np.sum(overallPredictions == testingOut)+0.0)/len(testingOut))



# TODO
# Predict the type of rest
def predictRest(testingInput):
	return


# TODO
# Predict the type of extra note - sharp or flat
def predictExtra(testingInput):
	return


# TODO
# Predict the type of real note - eighth, half, quarter, whole
def predictRealNote(testingInput):
	return


# TODO
# Predict the type of the note - from all notes - call the respective neural net for prediction
def predictNote(symbol):
	# what type of note
	res = None
	
	if res == 'realNote':
		return predictRealNote(symbol)
	if res == 'rest':
		return predictRest(symbol)
	elif res == 'extra':
		return predictExtra(symbol)



# @testingInput - 2d numpy array of testing inputs
# @testingOutput - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the overall neural network
def checkPredictions(testingInput, testingOut):

	stringOutputs = []
	# label the testing output correctly for identification
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		translation = translations[output]

		if translation == 'C-Clef' or translation == 'G-Clef' or translation == 'F-Clef':
			# for clef
			stringOutputs.append(translation)
		else:
			# for note
			stringOutputs.append('NOTE')

	incorrect = 0
	correct = 0

	for t in range(0, testingInput.shape[0], 100):

		test = testingInput[t].reshape((1, 3500))
		prediction = predict(test)

		print("PREDICTION: ", prediction[0], "ACTUAL:", stringOutputs[t])

		if prediction[0] == stringOutputs[t]:
			correct += 1
		else:
			incorrect += 1

	print("Accuracy: ", (correct + 0.0)/(correct + incorrect))



# @testingInput - 2d numpy array of testing input
# @return - prediction for given note
# Does the prediction for the given notes
def predict(testingIn):
	model = load_model('general_model.h5')

	# actual values for which one of the different types it could be
	generalPredictions = model.predict(testingIn)

	# actual value of the predictions
	overallPredictions = -np.ones((testingIn.shape[0],1))

	# predicted values of the strings
	stringPredictions = []

	for i in range(generalPredictions.shape[0]):
		overallPredictions[i] = np.argmax(generalPredictions[i])

		if overallPredictions[i] == 0:
			# send to the clef neural network
			clefPrediction = predictClef(testingIn)

			if clefPrediction[0] == 0:
				stringPredictions.append(translations[1])
			elif clefPrediction[0] == 1:
				stringPredictions.append(translations[6])
			else:
				stringPredictions.append(translations[8])

		else:
			# send to the note neural network
			notePrediction = predictNote(testingIn)
			stringPredictions.append('NOTE')

	return stringPredictions



if __name__ == '__main__':

	trainingIn, trainingOut, testingIn, testingOut = getData()
	# trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut)
	# testGeneralNN(testingIn, testingOut)
	# trainClefNN(trainingIn, trainingOut, testingIn, testingOut)
	# testClefNN(testingIn, testingOut)
	checkPredictions(testingIn, testingOut)
