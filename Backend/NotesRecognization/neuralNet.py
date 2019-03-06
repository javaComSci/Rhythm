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
translations = np.load('translationsWithLines.npy')
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
	[ [70, 'relu'], [30, 'relu'], [3, 'softmax'] ],
	[ [20, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [25, 'relu'], [5, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	[ [10, 'relu'], [3, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(clefTrainingIn, clefTrainingOut, clefTestingIn, clefTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam')

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
		# print("Prediction:", overallPredictions[i], "True Label", clefTestingOut[i])

		# showing the incorrect image
		# if overallPredictions[i] != clefTestingOut[i]:
		# 	testing = clefTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		if i % 99 == 0 and overallPredictions[i] == clefTestingOut[i]:
			print("Prediction:", overallPredictions[i], "True Label", clefTestingOut[i])
			testing = clefTestingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()
			

	print("Accuracy on clef testing data:", (np.sum(overallPredictions == clefTestingOut)+0.0)/len(clefTestingOut))


# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with notes, sharp/flat, rests
def trainNoteNN(trainingIn, trainingOut, testingIn, testingOut):
	# just need the notes and need to separate by the different notes there are 

	# modify the labels for notes, sharp/flat, and rests in all training data first
	for t in range(0, len(trainingOut)):
		output = trainingOut[t][0]
		
		translation = translations[output]
		if translation == 'Flat' or translation == 'Sharp':
			# for sharp/flat
			trainingOut[t][0] = -1
		elif translation == 'Whole-Note' or translation == 'Eighth-Note' or translation == 'Half-Note' or translation == 'Sixteenth-Note' or translation == 'Quarter-Note':
			# for actual notes
			trainingOut[t][0] = -2
		elif translation == 'Whole-Half-Rest' or translation == 'Eighth-Rest' or translation == 'Quarter-Rest':
			# for the rests
			trainingOut[t][0] = -3

	# modify the labels for notes, sharp/flat, and rests in all training data first
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'Flat' or translation == 'Sharp':
			# for sharp/flat
			testingOut[t][0] = -1
		elif translation == 'Whole-Note' or translation == 'Eighth-Note' or translation == 'Half-Note' or translation == 'Sixteenth-Note' or translation == 'Quarter-Note':
			# for actual notes
			testingOut[t][0] = -2
		elif translation == 'Whole-Half-Rest' or translation == 'Eighth-Rest' or translation == 'Quarter-Rest':
			# for the rests
			testingOut[t][0] = -3


	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	extrasIndiciesTraining = np.where(trainingOut == -1)[0]
	realNotesIndiciesTraining = np.where(trainingOut == -2)[0]
	restsIndiciesTraining = np.where(trainingOut == -3)[0]

	# for inputs
	notesTrainingIn = trainingIn[extrasIndiciesTraining]
	notesTrainingIn = np.vstack((notesTrainingIn, trainingIn[realNotesIndiciesTraining]))
	notesTrainingIn = np.vstack((notesTrainingIn, trainingIn[restsIndiciesTraining]))

	# for outputs
	notesTrainingOut = trainingOut[extrasIndiciesTraining,:]
	notesTrainingOut = np.vstack((notesTrainingOut, trainingOut[realNotesIndiciesTraining,:]))
	notesTrainingOut = np.vstack((notesTrainingOut, trainingOut[restsIndiciesTraining,:]))

	# changing values
	notesTrainingOut[notesTrainingOut == -1] = 0
	notesTrainingOut[notesTrainingOut == -2] = 1
	notesTrainingOut[notesTrainingOut == -3] = 2


	# TESTING DATA CLEANING
	# row indicies so need the [0]
	extrasIndiciesTesting = np.where(testingOut == -1)[0]
	realNotesIndiciesTesting = np.where(testingOut == -2)[0]
	restsIndiciesTesting = np.where(testingOut == -3)[0]

	# for inputs
	notesTestingIn = testingIn[extrasIndiciesTesting]
	notesTestingIn = np.vstack((notesTestingIn, testingIn[realNotesIndiciesTesting]))
	notesTestingIn = np.vstack((notesTestingIn, testingIn[restsIndiciesTesting]))

	# for outputs
	notesTestingOut = testingOut[extrasIndiciesTesting,:]
	notesTestingOut = np.vstack((notesTestingOut, testingOut[realNotesIndiciesTesting,:]))
	notesTestingOut = np.vstack((notesTestingOut, testingOut[restsIndiciesTesting,:]))

	# changing values
	notesTestingOut[notesTestingOut == -1] = 0
	notesTestingOut[notesTestingOut == -2] = 1
	notesTestingOut[notesTestingOut == -3] = 2


	print("SHAPES", notesTestingIn.shape, notesTestingOut.shape, notesTrainingIn.shape, notesTrainingOut.shape)
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [20, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [25, 'relu'], [5, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	[ [10, 'relu'], [3, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(notesTrainingIn, notesTrainingOut, notesTestingIn, notesTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam')

	# save the model for later use
	model.save('notes_model.h5')


# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network for the base
def testNoteNN(testingIn, testingOut):
	model = load_model('notes_model.h5')

	# modify the labels for notes, sharp/flat, and rests in all training data first
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'Flat' or translation == 'Sharp':
			# for sharp/flat
			testingOut[t][0] = -1
		elif translation == 'Whole-Note' or translation == 'Eighth-Note' or translation == 'Half-Note' or translation == 'Sixteenth-Note' or translation == 'Quarter-Note':
			# for actual notes
			testingOut[t][0] = -2
		elif translation == 'Whole-Half-Rest' or translation == 'Eighth-Rest' or translation == 'Quarter-Rest':
			# for the rests
			testingOut[t][0] = -3


	# TESTING DATA CLEANING
	# row indicies so need the [0]
	extrasIndiciesTesting = np.where(testingOut == -1)[0]
	realNotesIndiciesTesting = np.where(testingOut == -2)[0]
	restsIndiciesTesting = np.where(testingOut == -3)[0]

	# for inputs
	notesTestingIn = testingIn[extrasIndiciesTesting]
	notesTestingIn = np.vstack((notesTestingIn, testingIn[realNotesIndiciesTesting]))
	notesTestingIn = np.vstack((notesTestingIn, testingIn[restsIndiciesTesting]))

	# for outputs
	notesTestingOut = testingOut[extrasIndiciesTesting,:]
	notesTestingOut = np.vstack((notesTestingOut, testingOut[realNotesIndiciesTesting,:]))
	notesTestingOut = np.vstack((notesTestingOut, testingOut[restsIndiciesTesting,:]))

	# changing values
	notesTestingOut[notesTestingOut == -1] = 0
	notesTestingOut[notesTestingOut == -2] = 1
	notesTestingOut[notesTestingOut == -3] = 2


	# predictions on unseen data
	predictions = model.predict(notesTestingIn)
	overallPredictions = -np.ones((len(notesTestingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", notesTestingOut[i])

		# showing the incorrect image
		# if overallPredictions[i] != notesTestingOut[i]:
		# 	testing = notesTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		# if i % 99 == 0 and overallPredictions[i] == notesTestingOut[i]:
		# 	print("Prediction:", overallPredictions[i], "True Label", notesTestingOut[i])
		# 	testing = notesTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
			

	print("Accuracy on notes testing data:", (np.sum(overallPredictions == notesTestingOut)+0.0)/len(notesTestingOut))


# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with distinguishing between different rests
def trainExtrasNN(trainingIn, trainingOut, testingIn, testingOut):
	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	sharpIndiciesTraining = np.where(trainingOut == 0)[0]
	flatIndiciesTraining = np.where(trainingOut == 12)[0]

	# for inputs
	extraTrainingIn = trainingIn[sharpIndiciesTraining]
	extraTrainingIn = np.vstack((extraTrainingIn, trainingIn[flatIndiciesTraining]))

	# for outputs
	extraTrainingOut = trainingOut[sharpIndiciesTraining,:]
	extraTrainingOut = np.vstack((extraTrainingOut, trainingOut[flatIndiciesTraining]))

	# changing values
	extraTrainingOut[extraTrainingOut == 0] = 0
	extraTrainingOut[extraTrainingOut == 12] = 1


	#TESTING DATA CLEANING
	# row indicies
	sharpIndiciesTesting = np.where(testingOut == 0)[0]
	flatIndiciesTesting = np.where(testingOut == 12)[0]

	# for inputs
	extraTestingIn = testingIn[sharpIndiciesTesting]
	extraTestingIn = np.vstack((extraTestingIn, testingIn[flatIndiciesTesting]))

	# for outputs
	extraTestingOut = testingOut[sharpIndiciesTesting,:]
	extraTestingOut = np.vstack((extraTestingOut, testingOut[flatIndiciesTesting]))

	# changing values
	extraTestingOut[extraTestingOut == 0] = 0
	extraTestingOut[extraTestingOut == 12] = 1

	print("SHAPES", extraTestingIn.shape, extraTestingOut.shape, extraTrainingIn.shape, extraTrainingOut.shape)
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [70, 'relu'], [30, 'relu'], [3, 'softmax'] ],
	[ [90, 'relu'], [40, 'relu'], [3, 'softmax'] ],
	[ [100, 'relu'], [50, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(extraTrainingIn, extraTrainingOut, extraTestingIn, extraTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=10)

	# save the model for later use
	model.save('extras_model.h5')


# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network trained with sharps/falts
def testExtrasNN(testingIn, testingOut):
	model = load_model('extras_model.h5')

	#TESTING DATA CLEANING
	# row indicies
	sharpIndiciesTesting = np.where(testingOut == 0)[0]
	flatIndiciesTesting = np.where(testingOut == 12)[0]

	# for inputs
	extraTestingIn = testingIn[sharpIndiciesTesting]
	extraTestingIn = np.vstack((extraTestingIn, testingIn[flatIndiciesTesting]))

	# for outputs
	extraTestingOut = testingOut[sharpIndiciesTesting,:]
	extraTestingOut = np.vstack((extraTestingOut, testingOut[flatIndiciesTesting]))

	# changing values
	extraTestingOut[extraTestingOut == 0] = 0
	extraTestingOut[extraTestingOut == 12] = 1

	# predictions on unseen data
	predictions = model.predict(extraTestingIn)
	overallPredictions = -np.ones((len(extraTestingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", extraTestingOut[i])

		# showing the incorrect extraTestingOut
		# if overallPredictions[i] != extraTestingOut[i]:
		# 	testing = extraTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		# if i % 50 == 0 and overallPredictions[i] == extraTestingOut[i]:
		# 	print("Prediction:", overallPredictions[i], "True Label", extraTestingOut[i])
		# 	testing = extraTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
			

	print("Accuracy on extras testing data:", (np.sum(overallPredictions == extraTestingOut)+0.0)/len(extraTestingOut))


# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with distinguishing between different rests
def trainRestNN(trainingIn, trainingOut, testingIn, testingOut):
	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	eighthIndiciesTraining = np.where(trainingOut == 7)[0]
	quarterIndiciesTraining = np.where(trainingOut == 3)[0]
	halfIndiciesTraining = np.where(trainingOut == 4)[0]

	# for inputs
	restTrainingIn = trainingIn[eighthIndiciesTraining]
	restTrainingIn = np.vstack((restTrainingIn, trainingIn[quarterIndiciesTraining]))
	restTrainingIn = np.vstack((restTrainingIn, trainingIn[halfIndiciesTraining]))

	# for outputs
	restTrainingOut = trainingOut[eighthIndiciesTraining,:]
	restTrainingOut = np.vstack((restTrainingOut, trainingOut[quarterIndiciesTraining]))
	restTrainingOut = np.vstack((restTrainingOut, trainingOut[halfIndiciesTraining]))

	# changing values
	restTrainingOut[restTrainingOut == 7] = 0
	restTrainingOut[restTrainingOut == 3] = 1
	restTrainingOut[restTrainingOut == 4] = 2


	#TESTING DATA CLEANING
	# row indicies
	eighthIndiciesTesting = np.where(testingOut == 7)[0]
	quarterIndiciesTesting = np.where(testingOut == 3)[0]
	halfIndiciesTesting = np.where(testingOut == 4)[0]

	# for inputs
	restTestingIn = testingIn[eighthIndiciesTesting]
	restTestingIn = np.vstack((restTestingIn, testingIn[quarterIndiciesTesting]))
	restTestingIn = np.vstack((restTestingIn, testingIn[halfIndiciesTesting]))

	# for outputs
	restTestingOut = testingOut[eighthIndiciesTesting,:]
	restTestingOut = np.vstack((restTestingOut, testingOut[quarterIndiciesTesting]))
	restTestingOut = np.vstack((restTestingOut, testingOut[halfIndiciesTesting]))

	# changing values
	restTestingOut[restTestingOut == 7] = 0
	restTestingOut[restTestingOut == 3] = 1
	restTestingOut[restTestingOut == 4] = 2

	print("SHAPES", restTestingIn.shape, restTestingOut.shape, restTrainingIn.shape, restTrainingOut.shape)
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [3, 'softmax'] ],
	[ [70, 'relu'], [30, 'relu'], [3, 'softmax'] ],
	[ [90, 'relu'], [40, 'relu'], [3, 'softmax'] ],
	[ [100, 'relu'], [50, 'relu'], [3, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [3, 'softmax'] ],
	[ [50, 'sigmoid'], [3, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(restTrainingIn, restTrainingOut, restTestingIn, restTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=15)

	# save the model for later use
	model.save('rest_model.h5')



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with distingiusihing between real notes
def trainRealNoteNN(trainingIn, trainingOut, testingIn, testingOut):
	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	sixteenthIndiciesTraining = np.where(trainingOut == 10)[0]
	eighthIndiciesTraining = np.where(trainingOut == 5)[0]
	quarterIndiciesTraining = np.where(trainingOut == 11)[0]
	halfIndiciesTraining = np.where(trainingOut == 9)[0]
	wholeIndiciesTraining = np.where(trainingOut == 2)[0]

	# for inputs
	realNoteTrainingIn = trainingIn[sixteenthIndiciesTraining]
	realNoteTrainingIn = np.vstack((realNoteTrainingIn, trainingIn[eighthIndiciesTraining]))
	realNoteTrainingIn = np.vstack((realNoteTrainingIn, trainingIn[quarterIndiciesTraining]))
	realNoteTrainingIn = np.vstack((realNoteTrainingIn, trainingIn[halfIndiciesTraining]))
	realNoteTrainingIn = np.vstack((realNoteTrainingIn, trainingIn[wholeIndiciesTraining]))

	# for outputs
	realNoteTrainingOut = trainingOut[sixteenthIndiciesTraining,:]
	realNoteTrainingOut = np.vstack((realNoteTrainingOut, trainingOut[eighthIndiciesTraining]))
	realNoteTrainingOut = np.vstack((realNoteTrainingOut, trainingOut[quarterIndiciesTraining]))
	realNoteTrainingOut = np.vstack((realNoteTrainingOut, trainingOut[halfIndiciesTraining]))
	realNoteTrainingOut = np.vstack((realNoteTrainingOut, trainingOut[wholeIndiciesTraining]))

	# changing values
	realNoteTrainingOut[realNoteTrainingOut == 10] = 0
	realNoteTrainingOut[realNoteTrainingOut == 5] = 1
	realNoteTrainingOut[realNoteTrainingOut == 11] = 2
	realNoteTrainingOut[realNoteTrainingOut == 9] = 3
	realNoteTrainingOut[realNoteTrainingOut == 2] = 4


	#TESTING DATA CLEANING
	# row indicies
	sixteenthIndiciesTesting = np.where(testingOut == 10)[0]
	eighthIndiciesTesting = np.where(testingOut == 5)[0]
	quarterIndiciesTesting = np.where(testingOut == 11)[0]
	halfIndiciesTesting = np.where(testingOut == 9)[0]
	wholeIndiciesTesting = np.where(testingOut == 2)[0]

	# for inputs
	realNoteTestingIn = testingIn[sixteenthIndiciesTesting]
	realNoteTestingIn = np.vstack((realNoteTestingIn, testingIn[eighthIndiciesTesting]))
	realNoteTestingIn = np.vstack((realNoteTestingIn, testingIn[quarterIndiciesTesting]))
	realNoteTestingIn = np.vstack((realNoteTestingIn, testingIn[halfIndiciesTesting]))
	realNoteTestingIn = np.vstack((realNoteTestingIn, testingIn[wholeIndiciesTesting]))

	# for outputs
	realNoteTestingOut = testingOut[sixteenthIndiciesTesting,:]
	realNoteTestingOut = np.vstack((realNoteTestingOut, testingOut[eighthIndiciesTesting]))
	realNoteTestingOut = np.vstack((realNoteTestingOut, testingOut[quarterIndiciesTesting]))
	realNoteTestingOut = np.vstack((realNoteTestingOut, testingOut[halfIndiciesTesting]))
	realNoteTestingOut = np.vstack((realNoteTestingOut, testingOut[wholeIndiciesTesting]))

	# changing values
	realNoteTestingOut[realNoteTestingOut == 10] = 0
	realNoteTestingOut[realNoteTestingOut == 5] = 1
	realNoteTestingOut[realNoteTestingOut == 11] = 2
	realNoteTestingOut[realNoteTestingOut == 9] = 3
	realNoteTestingOut[realNoteTestingOut == 2] = 4

	# print("TRAINING", cclefIndiciesTraining, gclefIndiciesTraining, fclefIndiciesTraining, clefTrainingIn, clefTrainingIn.shape, clefTrainingOut, clefTrainingOut.shape)
	# print("TESTING", clefTestingIn.shape, clefTestingIn, clefTestingOut, clefTestingOut.shape)

	print("SHAPES", realNoteTestingIn.shape, realNoteTestingOut.shape, realNoteTrainingIn.shape, realNoteTrainingOut.shape)
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [5, 'softmax'] ],
	[ [70, 'relu'], [30, 'relu'], [5, 'softmax'] ],
	[ [60, 'relu'], [50, 'relu'], [5, 'softmax'] ],
	[ [100, 'relu'], [50, 'relu'], [5, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(realNoteTrainingIn, realNoteTrainingOut, realNoteTestingIn, realNoteTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=20)

	# save the model for later use
	model.save('real_note_model.h5')


# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @modelIfo - array of models with layer info for each model of form [[[numNeurons,activationFunction],....]]
# @return - neural network model
# Add layers to sequential model, compile model, and fit the model
def trainModel(trainingIn, trainingOut, modelInfo, lossInfo, optInfo, epochs = 15):
	# create model sequential
	model = Sequential()

	# add first layer
	model.add(Dense(modelInfo[0][0], input_dim=3500, activation=modelInfo[0][1]))

	# each layer is given activation function and number of neurons
	for i in range(1, len(modelInfo)):
		model.add(Dense(modelInfo[i][0], activation=modelInfo[i][1]))

	# compile the model with optimizer
	model.compile(loss=lossInfo, optimizer=optInfo, metrics=['accuracy'])

	model.summary()

	# train the model
	model.fit(trainingIn, trainingOut, epochs=epochs)

	return model



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @modelIfo - array of models with layer info for each model of form [[[numNeurons,activationFunction],....]]
# @return - neural network model
# Do hyperparameter tuning to find the best hyperparameters for a model
def hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, modelsInfo, optInfo, lossInfo, epochs = 15):
	# stores the best model after hyperparamter tuning
	bestModel = None
	bestTestAcc = -math.inf
	allModels = {}

	modelCount = 0
	# go through all models to be trained with
	for modelInfo in modelsInfo:
		
		# create and traing a model
		model = trainModel(trainingIn, trainingOut, modelInfo, optInfo, lossInfo, epochs)

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


	# create the layers that could be used for hyperparameter tuning - categorical cross enrotpy
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [2, 'softmax'] ],
	[ [20, 'relu'], [15, 'tanh'], [2, 'softmax'] ],
	[ [50, 'relu'], [2, 'softmax'] ],
	[ [40, 'tanh'], [2, 'softmax'] ],
	[ [50, 'sigmoid'], [2, 'softmax'] ],
	]

	# create the layers that could be used for hyperparameter tuning - binary cross entorpy
	# layersForTraining = [ [[50, 'relu'], [20, 'relu'], [2, 'softmax'] ],
	# [ [20, 'relu'], [15, 'tanh'], [2, 'softmax'] ],
	# [ [50, 'relu'], [2, 'softmax'] ],
	# [ [40, 'tanh'], [2, 'softmax'] ],
	# [ [50, 'sigmoid'], [2, 'softmax'] ],
	# [ [300, 'relu'], [2, 'softmax'] ],
	# ]

	# perform hyperparameter tuning
	model = hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam')

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
		if i % 1000 == 0 and overallPredictions[i] == testingOut[i]:
			testing = testingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()

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

		print("PREDICTION: ", prediction[0][0], "ACTUAL:", stringOutputs[t])

		# testing = testingInput[t]
		# testing = testing * 255
		# testing = testing.reshape(70, 50)
		# img = Image.fromarray(testing)
		# img.show()

		if prediction[0][0] == stringOutputs[t]:
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

	return stringPredictions, testingIn



if __name__ == '__main__':

	trainingIn, trainingOut, testingIn, testingOut = getData()
	# trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut)
	# testGeneralNN(testingIn, testingOut)
	# trainClefNN(trainingIn, trainingOut, testingIn, testingOut)
	# testClefNN(testingIn, testingOut)
	# trainNoteNN(trainingIn, trainingOut, testingIn, testingOut)
	# testNoteNN(testingIn, testingOut)
	trainRealNoteNN(trainingIn, trainingOut, testingIn, testingOut)
	# trainRestNN(trainingIn, trainingOut, testingIn, testingOut)
	# trainExtrasNN(trainingIn, trainingOut, testingIn, testingOut)
	# testExtrasNN(testingIn, testingOut)
	# checkPredictions(testingIn, testingOut)
