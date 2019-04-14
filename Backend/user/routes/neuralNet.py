import tensorflow as tf
from tensorflow import keras
from tensorflow import Graph, Session
import numpy as np
from keras.models import Sequential
import cv2
from PIL import Image
from keras.layers import Dense, Dropout
from keras.models import load_model
import math
import os
from noteNeuralNet import predictNote
from clefNeuralNet import predictClef
from realNoteNeuralNet import predictRealNote
from extrasNeuralNet import predictExtraNote
from restNeuralNet import predictRest
os.environ['KMP_DUPLICATE_LIB_OK']='True'


# load all translations
translations = np.load('/home/Rhythm/Backend/user/routes/translationsWithLines.npy')
translations = translations.item()

# create the inversion of the translations for value by key
translationsInverse = dict([v,k] for k,v in translations.items())

print("TRANLSATIONS", translations)
print("TRANLSATIONS INVERSE", translationsInverse)

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
# def getData():
# 	# data with lines
# 	trainingIn = np.load('/home/Rhythm/Backend/user/routes/trainingInWithLines.npy')
# 	trainingOut = np.load('/home/Rhythm/Backend/user/routes/trainingOutWithLines.npy')
# 	testingIn = np.load('/home/Rhythm/Backend/user/routes/testingInWithLines.npy')
# 	testingOut = np.load('/home/Rhythm/Backend/user/routes/testingOutWithLines.npy')

# 	# print("TRAINING IN")
# 	# for i in testingIn[0]:
# 		# print(i)

# 	return trainingIn, trainingOut, testingIn, testingOut



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
		if translation == 'CClef' or translation == 'GClef' or translation == 'FClef':
			# for clef
			trainingOut[t][0] = 0
		else:
			# for note
			trainingOut[t][0] = 1


	# modify the labels for clefs, notes, and times for testing data
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'CClef' or translation == 'GClef' or translation == 'FClef':
			# for clef
			testingOut[t][0] = 0
		else:
			# for note
			testingOut[t][0] = 1


	# create the layers that could be used for hyperparameter tuning - categorical cross enrotpy
	# layersForTraining = [ [[50, 'relu'], [20, 'relu'], [2, 'softmax'] ],
	# [ [20, 'relu'], [15, 'tanh'], [2, 'softmax'] ],
	# [ [50, 'relu'], [2, 'softmax'] ],
	# [ [40, 'tanh'], [2, 'softmax'] ],
	# [ [50, 'sigmoid'], [2, 'softmax'] ],
	# ]

	# create the layers that could be used for hyperparameter tuning - binary cross enrotpy
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [1, 'sigmoid'] ],
	[ [20, 'relu'], [15, 'tanh'], [1, 'sigmoid'] ],
	[ [50, 'relu'], [1, 'sigmoid'] ],
	[ [40, 'tanh'], [1, 'sigmoid'] ],
	[ [50, 'sigmoid'], [1, 'sigmoid'] ],
	]

	# perform hyperparameter tuning
	# model = hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=8)
	model = hyperparameterTuning(trainingIn, trainingOut, testingIn, testingOut, layersForTraining, 'binary_crossentropy', 'adam', epochs=8)

	# save the best model for the general NN
	model.save('general_model.h5')



# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network for the base
def testGeneralNN(testingIn, testingOut):

	# load the general model for testing
	model = load_model('/home/Rhythm/Backend/user/routes/general_model.h5')

	# modify the labels for clefs, notes, and times for testing data
	for t in range(0, len(testingOut)):
		output = testingOut[t][0]
		
		translation = translations[output]
		if translation == 'CClef' or translation == 'GClef' or translation == 'FClef':
			# for clef
			testingOut[t][0] = 0
		else:
			# for note
			testingOut[t][0] = 1

	# predictions on unseen data
	predictions = model.predict(testingIn)
	overallPredictions = -np.ones((len(testingOut),1))

	for i in range(predictions.shape[0]):
		# predictions with categorical cross entorpy
		# overallPredictions[i] = np.argmax(predictions[i])

		# predictions with binary classification
		if predictions[i] > .5:
			overallPredictions[i] = 1
		else:
			overallPredictions[i] = 0

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
		if i % 200 == 0 and overallPredictions[i] != testingOut[i]:
			testing = testingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()

	print("Accuracy on general testing data:", (np.sum(overallPredictions == testingOut)+0.0)/len(testingOut))



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with identifying the different clefs
def trainClefNN(trainingIn, trainingOut, testingIn, testingOut):

	cclef = translationsInverse["CClef"]
	gclef = translationsInverse["GClef"]
	fclef = translationsInverse["FClef"]

	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	cclefIndiciesTraining = np.where(trainingOut == cclef)[0]
	gclefIndiciesTraining = np.where(trainingOut == gclef)[0]
	fclefIndiciesTraining = np.where(trainingOut == fclef)[0]

	# for inputs
	clefTrainingIn = trainingIn[cclefIndiciesTraining]
	clefTrainingIn = np.vstack((clefTrainingIn, trainingIn[gclefIndiciesTraining]))
	clefTrainingIn = np.vstack((clefTrainingIn, trainingIn[fclefIndiciesTraining]))

	# for outputs
	clefTrainingOut = trainingOut[cclefIndiciesTraining,:]
	clefTrainingOut = np.vstack((clefTrainingOut, trainingOut[gclefIndiciesTraining,:]))
	clefTrainingOut = np.vstack((clefTrainingOut, trainingOut[fclefIndiciesTraining,:]))

	# changing values so no confusion with overlaps
	clefTrainingOut[clefTrainingOut == cclef] = -1
	clefTrainingOut[clefTrainingOut == gclef] = -2
	clefTrainingOut[clefTrainingOut == fclef] = -3

	# change back to normalized
	clefTrainingOut[clefTrainingOut == -1] = 0
	clefTrainingOut[clefTrainingOut == -2] = 1
	clefTrainingOut[clefTrainingOut == -3] = 2


	#TESTING DATA CLEANING
	# row indicies
	cclefIndiciesTesting = np.where(testingOut == cclef)[0]
	gclefIndiciesTesting = np.where(testingOut == gclef)[0]
	fclefIndiciesTesting = np.where(testingOut == fclef)[0]

	# for inputs
	clefTestingIn = testingIn[cclefIndiciesTesting]
	clefTestingIn = np.vstack((clefTestingIn, testingIn[gclefIndiciesTesting]))
	clefTestingIn = np.vstack((clefTestingIn, testingIn[fclefIndiciesTesting]))

	# for outputs
	clefTestingOut = testingOut[cclefIndiciesTesting,:]
	clefTestingOut = np.vstack((clefTestingOut, testingOut[gclefIndiciesTesting,:]))
	clefTestingOut = np.vstack((clefTestingOut, testingOut[fclefIndiciesTesting,:]))

	# changing values
	clefTestingOut[clefTestingOut == cclef] = -1
	clefTestingOut[clefTestingOut == gclef] = -2
	clefTestingOut[clefTestingOut == fclef] = -3

	clefTestingOut[clefTestingOut == -1] = 0
	clefTestingOut[clefTestingOut == -2] = 1
	clefTestingOut[clefTestingOut == -3] = 2


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
	model = hyperparameterTuning(clefTrainingIn, clefTrainingOut, clefTestingIn, clefTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=8)

	# save the model for later use
	model.save('/home/Rhythm/Backend/user/routes/clef_model.h5')



# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network trained with clefs
def testClefNN(testingIn, testingOut):
	model = load_model('/home/Rhythm/Backend/user/routes/clef_model.h5')

	cclef = translationsInverse["CClef"]
	gclef = translationsInverse["GClef"]
	fclef = translationsInverse["FClef"]


	#TESTING DATA CLEANING
	# row indicies
	cclefIndiciesTesting = np.where(testingOut == cclef)[0]
	gclefIndiciesTesting = np.where(testingOut == gclef)[0]
	fclefIndiciesTesting = np.where(testingOut == fclef)[0]

	# for inputs
	clefTestingIn = testingIn[cclefIndiciesTesting]
	clefTestingIn = np.vstack((clefTestingIn, testingIn[gclefIndiciesTesting]))
	clefTestingIn = np.vstack((clefTestingIn, testingIn[fclefIndiciesTesting]))

	# for outputs
	clefTestingOut = testingOut[cclefIndiciesTesting,:]
	clefTestingOut = np.vstack((clefTestingOut, testingOut[gclefIndiciesTesting,:]))
	clefTestingOut = np.vstack((clefTestingOut, testingOut[fclefIndiciesTesting,:]))

	# changing values
	clefTestingOut[clefTestingOut == cclef] = -1
	clefTestingOut[clefTestingOut == gclef] = -2
	clefTestingOut[clefTestingOut == fclef] = -3

	clefTestingOut[clefTestingOut == -1] = 0
	clefTestingOut[clefTestingOut == -2] = 1
	clefTestingOut[clefTestingOut == -3] = 2

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
		if i % 999 == 0 and overallPredictions[i] == clefTestingOut[i]:
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
	model = hyperparameterTuning(notesTrainingIn, notesTrainingOut, notesTestingIn, notesTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=10)

	# save the model for later use
	model.save('/home/Rhythm/Backend/user/routes/notes_model.h5')



# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network for the base
def testNoteNN(testingIn, testingOut):
	model = load_model('/home/Rhythm/Backend/user/routes/notes_model.h5')

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
		# if i % 50 == 0 and overallPredictions[i] != notesTestingOut[i]:
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

	sharp = translationsInverse["Sharp"]
	flat = translationsInverse["Flat"]

	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	flatIndiciesTraining = np.where(trainingOut == flat)[0]
	sharpIndiciesTraining = np.where(trainingOut == sharp)[0]

	# for inputs
	extraTrainingIn = trainingIn[flatIndiciesTraining]
	extraTrainingIn = np.vstack((extraTrainingIn, trainingIn[sharpIndiciesTraining]))

	# for outputs
	extraTrainingOut = trainingOut[flatIndiciesTraining,:]
	extraTrainingOut = np.vstack((extraTrainingOut, trainingOut[sharpIndiciesTraining]))

	# changing values
	extraTrainingOut[extraTrainingOut == flat] = -1
	extraTrainingOut[extraTrainingOut == sharp] = -2

	extraTrainingOut[extraTrainingOut == -1] = 0
	extraTrainingOut[extraTrainingOut == -2] = 1


	#TESTING DATA CLEANING
	# row indicies
	sharpIndiciesTesting = np.where(testingOut == sharp)[0]
	flatIndiciesTesting = np.where(testingOut == flat)[0]

	# for inputs
	extraTestingIn = testingIn[flatIndiciesTesting]
	extraTestingIn = np.vstack((extraTestingIn, testingIn[sharpIndiciesTesting]))

	# for outputs
	extraTestingOut = testingOut[flatIndiciesTesting,:]
	extraTestingOut = np.vstack((extraTestingOut, testingOut[sharpIndiciesTesting]))

	# flat is originally 0, so keep it as 0
	# changing values
	extraTestingOut[extraTestingOut == flat] = -1
	extraTestingOut[extraTestingOut == sharp] = -2

	extraTestingOut[extraTestingOut == -1] = 0
	extraTestingOut[extraTestingOut == -2] = 1


	print("SHAPES", extraTestingIn.shape, extraTestingOut.shape, extraTrainingIn.shape, extraTrainingOut.shape)
	

	# setup layers for hyperparameter tuning
	layersForTraining = [ [[50, 'relu'], [20, 'relu'], [2, 'softmax'] ],
	[ [70, 'relu'], [30, 'relu'], [2, 'softmax'] ],
	[ [90, 'relu'], [40, 'relu'], [2, 'softmax'] ],
	[ [100, 'relu'], [50, 'relu'], [2, 'softmax'] ],
	[ [30, 'relu'], [15, 'relu'], [2, 'softmax'] ],
	[ [50, 'sigmoid'], [2, 'softmax'] ],
	]

	# obtain the best model from hyperparameter tuning
	model = hyperparameterTuning(extraTrainingIn, extraTrainingOut, extraTestingIn, extraTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=5)

	# save the model for later use
	model.save('/home/Rhythm/Backend/user/routes/extras_model.h5')


# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the neural network trained with sharps/falts
def testExtrasNN(testingIn, testingOut):
	model = load_model('/home/Rhythm/Backend/user/routes/extras_model.h5')

	sharp = translationsInverse["Sharp"]
	flat = translationsInverse["Flat"]

	#TESTING DATA CLEANING
	# row indicies
	sharpIndiciesTesting = np.where(testingOut == sharp)[0]
	flatIndiciesTesting = np.where(testingOut == flat)[0]

	# for inputs
	extraTestingIn = testingIn[flatIndiciesTesting]
	extraTestingIn = np.vstack((extraTestingIn, testingIn[sharpIndiciesTesting]))

	# for outputs
	extraTestingOut = testingOut[flatIndiciesTesting,:]
	extraTestingOut = np.vstack((extraTestingOut, testingOut[sharpIndiciesTesting]))

	# flat is originally 0, so keep it as 0
	# changing values
	extraTestingOut[extraTestingOut == flat] = -1
	extraTestingOut[extraTestingOut == sharp] = -2

	extraTestingOut[extraTestingOut == -1] = 0
	extraTestingOut[extraTestingOut == -2] = 1

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
		if i % 50 == 0 and overallPredictions[i] == extraTestingOut[i]:
			print("Prediction:", overallPredictions[i], "True Label", extraTestingOut[i])
			testing = extraTestingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()
			

	print("Accuracy on extras testing data:", (np.sum(overallPredictions == extraTestingOut)+0.0)/len(extraTestingOut))



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with distinguishing between different rests
def trainRestNN(trainingIn, trainingOut, testingIn, testingOut):

	# get the inverse translations
	eighthRest = translationsInverse["Eighth-Rest"]
	quarterRest = translationsInverse["Quarter-Rest"]
	halfRest = translationsInverse["Whole-Half-Rest"]

	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	eighthIndiciesTraining = np.where(trainingOut == eighthRest)[0]
	quarterIndiciesTraining = np.where(trainingOut == quarterRest)[0]
	halfIndiciesTraining = np.where(trainingOut == halfRest)[0]

	# for inputs
	restTrainingIn = trainingIn[eighthIndiciesTraining]
	restTrainingIn = np.vstack((restTrainingIn, trainingIn[quarterIndiciesTraining]))
	restTrainingIn = np.vstack((restTrainingIn, trainingIn[halfIndiciesTraining]))

	# for outputs
	restTrainingOut = trainingOut[eighthIndiciesTraining,:]
	restTrainingOut = np.vstack((restTrainingOut, trainingOut[quarterIndiciesTraining]))
	restTrainingOut = np.vstack((restTrainingOut, trainingOut[halfIndiciesTraining]))

	# changing values
	restTrainingOut[restTrainingOut == eighthRest] = -1
	restTrainingOut[restTrainingOut == quarterRest] = -2
	restTrainingOut[restTrainingOut == halfRest] = -3

	restTrainingOut[restTrainingOut == -1] = 0
	restTrainingOut[restTrainingOut == -2] = 1
	restTrainingOut[restTrainingOut == -3] = 2


	#TESTING DATA CLEANING
	# row indicies
	eighthIndiciesTesting = np.where(testingOut == eighthRest)[0]
	quarterIndiciesTesting = np.where(testingOut == quarterRest)[0]
	halfIndiciesTesting = np.where(testingOut == halfRest)[0]

	# for inputs
	restTestingIn = testingIn[eighthIndiciesTesting]
	restTestingIn = np.vstack((restTestingIn, testingIn[quarterIndiciesTesting]))
	restTestingIn = np.vstack((restTestingIn, testingIn[halfIndiciesTesting]))

	# for outputs
	restTestingOut = testingOut[eighthIndiciesTesting,:]
	restTestingOut = np.vstack((restTestingOut, testingOut[quarterIndiciesTesting]))
	restTestingOut = np.vstack((restTestingOut, testingOut[halfIndiciesTesting]))

	# quarter is orignally at 1, so need to keep it at 1
	# changing values
	restTestingOut[restTestingOut == eighthRest] = -1
	restTestingOut[restTestingOut == quarterRest] = -2
	restTestingOut[restTestingOut == halfRest] = -3

	restTestingOut[restTestingOut == -1] = 0
	restTestingOut[restTestingOut == -2] = 1
	restTestingOut[restTestingOut == -3] = 2


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
	model = hyperparameterTuning(restTrainingIn, restTrainingOut, restTestingIn, restTestingOut, layersForTraining, 'sparse_categorical_crossentropy', 'adam', epochs=3)

	# save the model for later use
	model.save('/home/Rhythm/Backend/user/routes/rest_model.h5')


# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the real note network trained with the real notes
def testRestNN(testingIn, testingOut):
	model = load_model('/home/Rhythm/Backend/user/routes/rest_model.h5')

	# get the inverse translations
	eighthRest = translationsInverse["Eighth-Rest"]
	quarterRest = translationsInverse["Quarter-Rest"]
	halfRest = translationsInverse["Whole-Half-Rest"]

	#TESTING DATA CLEANING
	# row indicies
	eighthIndiciesTesting = np.where(testingOut == eighthRest)[0]
	quarterIndiciesTesting = np.where(testingOut == quarterRest)[0]
	halfIndiciesTesting = np.where(testingOut == halfRest)[0]

	# for inputs
	restTestingIn = testingIn[eighthIndiciesTesting]
	restTestingIn = np.vstack((restTestingIn, testingIn[quarterIndiciesTesting]))
	restTestingIn = np.vstack((restTestingIn, testingIn[halfIndiciesTesting]))

	# for outputs
	restTestingOut = testingOut[eighthIndiciesTesting,:]
	restTestingOut = np.vstack((restTestingOut, testingOut[quarterIndiciesTesting]))
	restTestingOut = np.vstack((restTestingOut, testingOut[halfIndiciesTesting]))

	# quarter is orignally at 1, so need to keep it at 1
	# changing values
	restTestingOut[restTestingOut == eighthRest] = -1
	restTestingOut[restTestingOut == quarterRest] = -2
	restTestingOut[restTestingOut == halfRest] = -3

	restTestingOut[restTestingOut == -1] = 0
	restTestingOut[restTestingOut == -2] = 1
	restTestingOut[restTestingOut == -3] = 2

	# predictions on unseen data
	predictions = model.predict(restTestingIn)
	overallPredictions = -np.ones((len(restTestingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", restTestingOut[i])

		# showing the incorrect image
		# if overallPredictions[i] != restTestingOut[i]:
		# 	testing = restTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
		# 	break

		# show the example of the image and the value wanted
		if i % 70 == 0 and overallPredictions[i] == restTestingOut[i]:
			print("Prediction:", overallPredictions[i], "True Label", restTestingOut[i])
			testing = restTestingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()
			

	print("Accuracy on real note testing data:", (np.sum(overallPredictions == restTestingOut)+0.0)/len(restTestingOut))



# @trainingIn - 2d numpy array of training inputs
# @trainingOut - 2d numpy array of training labels
# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Trains neural network with distingiusihing between real notes
def trainRealNoteNN(trainingIn, trainingOut, testingIn, testingOut):

	# get the inverse translations
	sixteenthNote = translationsInverse["Sixteenth-Note"]
	eighthNote = translationsInverse["Eighth-Note"]
	quarterNote = translationsInverse["Quarter-Note"]
	halfNote = translationsInverse["Half-Note"]
	wholeNote = translationsInverse["Whole-Note"]

	# TRAINING DATA CLEANING
	# row indicies so need the [0]
	sixteenthIndiciesTraining = np.where(trainingOut == sixteenthNote)[0]
	eighthIndiciesTraining = np.where(trainingOut == eighthNote)[0]
	quarterIndiciesTraining = np.where(trainingOut == quarterNote)[0]
	halfIndiciesTraining = np.where(trainingOut == halfNote)[0]
	wholeIndiciesTraining = np.where(trainingOut == wholeNote)[0]

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
	realNoteTrainingOut[realNoteTrainingOut == sixteenthNote] = -1
	realNoteTrainingOut[realNoteTrainingOut == eighthNote] = -2
	realNoteTrainingOut[realNoteTrainingOut == quarterNote] = -3
	realNoteTrainingOut[realNoteTrainingOut == halfNote] = -4
	realNoteTrainingOut[realNoteTrainingOut == wholeNote] = -5

	realNoteTrainingOut[realNoteTrainingOut == -1] = 0
	realNoteTrainingOut[realNoteTrainingOut == -2] = 1
	realNoteTrainingOut[realNoteTrainingOut == -3] = 2
	realNoteTrainingOut[realNoteTrainingOut == -4] = 3
	realNoteTrainingOut[realNoteTrainingOut == -5] = 4


	#TESTING DATA CLEANING
	# row indicies
	sixteenthIndiciesTesting = np.where(testingOut == sixteenthNote)[0]
	eighthIndiciesTesting = np.where(testingOut == eighthNote)[0]
	quarterIndiciesTesting = np.where(testingOut == quarterNote)[0]
	halfIndiciesTesting = np.where(testingOut == halfNote)[0]
	wholeIndiciesTesting = np.where(testingOut == wholeNote)[0]

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
	realNoteTestingOut[realNoteTestingOut == sixteenthNote] = -1
	realNoteTestingOut[realNoteTestingOut == eighthNote] = -2
	realNoteTestingOut[realNoteTestingOut == quarterNote] = -3
	realNoteTestingOut[realNoteTestingOut == halfNote] = -4
	realNoteTestingOut[realNoteTestingOut == wholeNote] = -5

	realNoteTestingOut[realNoteTestingOut == -1] = 0
	realNoteTestingOut[realNoteTestingOut == -2] = 1
	realNoteTestingOut[realNoteTestingOut == -3] = 2
	realNoteTestingOut[realNoteTestingOut == -4] = 3
	realNoteTestingOut[realNoteTestingOut == -5] = 4

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
	model.save('/home/Rhythm/Backend/user/routes/real_note_model.h5')


# @testingIn - 2d numpy array of testing inputs
# @testingOut - 2d numpy array of testing labels
# @return - void
# Tests the accuracy of the real note network trained with the real notes
def testRealNoteNN(testingIn, testingOut):
	model = load_model('/home/Rhythm/Backend/user/routes/real_note_model.h5')

	# get the inverse translations
	sixteenthNote = translationsInverse["Sixteenth-Note"]
	eighthNote = translationsInverse["Eighth-Note"]
	quarterNote = translationsInverse["Quarter-Note"]
	halfNote = translationsInverse["Half-Note"]
	wholeNote = translationsInverse["Whole-Note"]

	#TESTING DATA CLEANING
	# row indicies
	sixteenthIndiciesTesting = np.where(testingOut == sixteenthNote)[0]
	eighthIndiciesTesting = np.where(testingOut == eighthNote)[0]
	quarterIndiciesTesting = np.where(testingOut == quarterNote)[0]
	halfIndiciesTesting = np.where(testingOut == halfNote)[0]
	wholeIndiciesTesting = np.where(testingOut == wholeNote)[0]

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
	realNoteTestingOut[realNoteTestingOut == sixteenthNote] = -1
	realNoteTestingOut[realNoteTestingOut == eighthNote] = -2
	realNoteTestingOut[realNoteTestingOut == quarterNote] = -3
	realNoteTestingOut[realNoteTestingOut == halfNote] = -4
	realNoteTestingOut[realNoteTestingOut == wholeNote] = -5

	realNoteTestingOut[realNoteTestingOut == -1] = 0
	realNoteTestingOut[realNoteTestingOut == -2] = 1
	realNoteTestingOut[realNoteTestingOut == -3] = 2
	realNoteTestingOut[realNoteTestingOut == -4] = 3
	realNoteTestingOut[realNoteTestingOut == -5] = 4

	# predictions on unseen data
	predictions = model.predict(realNoteTestingIn)
	overallPredictions = -np.ones((len(realNoteTestingOut),1))

	for i in range(predictions.shape[0]):
		overallPredictions[i] = np.argmax(predictions[i])
		print("Prediction:", overallPredictions[i], "True Label", realNoteTestingOut[i])

		# showing the incorrect image
		if i % 1 == 0 and overallPredictions[i] != realNoteTestingOut[i]:
			testing = realNoteTestingIn[i]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()
			break

		# show the example of the image and the value wanted
		# if i % 50 == 0 and overallPredictions[i] == realNoteTestingOut[i]:
		# 	print("Prediction:", overallPredictions[i], "True Label", realNoteTestingOut[i])
		# 	testing = realNoteTestingIn[i]
		# 	testing = testing * 255
		# 	testing = testing.reshape(70, 50)
		# 	img = Image.fromarray(testing)
		# 	img.show()
			

	print("Accuracy on real note testing data:", (np.sum(overallPredictions == realNoteTestingOut)+0.0)/len(realNoteTestingOut))



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
		stringOutputs.append(translation)

	incorrect = 0
	correct = 0

	for t in range(0, testingInput.shape[0], 30):

		test = testingInput[t].reshape((1, 3500))
		prediction = predict(test)

		print("PREDICTION: ", prediction[0][0], "ACTUAL:", stringOutputs[t])

		if prediction[0][0] == stringOutputs[t] and t % 60 == 0:
			testing = testingInput[t]
			testing = testing * 255
			testing = testing.reshape(70, 50)
			img = Image.fromarray(testing)
			img.show()

		if prediction[0][0] == stringOutputs[t]:
			correct += 1
		else:
			incorrect += 1


	print("Accuracy: ", (correct + 0.0)/(correct + incorrect))



# @testingInput - 2d numpy array of testing input
# @return - prediction for given note
# Does the prediction for the given notes
def predict(testingIn):

	# create a graph for the general prediction: NOTE or CLEF?
	generalPredGraph = Graph()

	with generalPredGraph.as_default():

		# open new session
		session1 = Session()

		with session1.as_default():

			# load general prediction model
			model = load_model('/home/Rhythm/Backend/user/routes/general_model.h5')

			# do the prediction with the general model
			generalPredictions = model.predict(testingIn)

			# actual value of the predictions
			overallPredictions = -np.ones((testingIn.shape[0],1))

			# predicted values of the strings
			stringPredictions = []

			# for each of the general predictions
			for i in range(generalPredictions.shape[0]):

				# find the value that was predicted

				overallPredictions[i] = np.argmax(generalPredictions[i])
				print("PREDICTION WAS", generalPredictions[i], generalPredictions[i][0])

				# find the value that was predicted
				# if generalPredictions[i][0] < 0.5:
					# overallPredictions[i] = 0
				# else:
					# overallPredictions[i] = 1

				# if it was a clef
				if overallPredictions[i] == 0:

					# create a graph for clef model: CCLEF, GCLEF, FCELF?
					clefPredGraph = Graph()

					with clefPredGraph.as_default():

						# create a new session for the clef
						session2 = Session()

						with session2.as_default():

							#load clef model
							model = load_model("/home/Rhythm/Backend/user/routes/clef_model.h5")

							# do the predictions with the clef model
							predictions = model.predict(testingIn)

							# find the clef prediction
							clefPrediction = np.argmax(predictions[i])
							print("Clef Prediction", predictions, clefPrediction)

							if clefPrediction == 0:
								stringPredictions.append('CClef')
							elif clefPrediction == 1:
								stringPredictions.append('GClef')
							elif clefPrediction == 2:
								stringPredictions.append('FClef')

							return stringPredictions, testingIn

				else:

					# find the general note - REAL NOTE, REST, EXTRA?
					notePredGraph = Graph()

					with notePredGraph.as_default():

						session3 = Session()

						with session3.as_default():

							#load general notes model
							model = load_model("/home/Rhythm/Backend/user/routes/notes_model.h5")

							# do the predictions on the notes model
							predictions = model.predict(testingIn)

							notePrediction = np.argmax(predictions[i])
							print("Note Prediction", predictions, notePrediction)

							# extras note
							if notePrediction == 0:

									# predict the extras - SHARP, FLAT?
									extrasPredGraph = Graph()

									with extrasPredGraph.as_default():

										session4 = Session()

										with session4.as_default():

											#load extras model
											model = load_model("/home/Rhythm/Backend/user/routes/extras_model.h5")

											predictions = model.predict(testingIn)

											extraPrediction = np.argmax(predictions[i])
											print("Extras Prediction", predictions)

											if extraPrediction == 0:
												stringPredictions.append('Flat')
											elif extraPrediction == 1:
												stringPredictions.append('Sharp')

											return stringPredictions, testingIn

							
							# real note
							elif notePrediction == 1:

								# real note graph - SIXTEENTH, EIGHTH, QUARTER, HALF, WHOLE
								realNotePredGraph = Graph()

								with realNotePredGraph.as_default():

									session5 = Session()

									with session5.as_default():

										#load model real note model
										model = load_model("/home/Rhythm/Backend/user/routes/real_note_model.h5")

										predictions = model.predict(testingIn)
	
										realNotePrediction = np.argmax(predictions[i])
										print("Real Note Prediction", predictions)

										if realNotePrediction == 0:
											stringPredictions.append('Sixteenth-Note')
										elif realNotePrediction == 1:
											stringPredictions.append('Eighth-Note')
										elif realNotePrediction == 2:
											stringPredictions.append('Quarter-Note')
										elif realNotePrediction == 3:
											stringPredictions.append('Half-Note')
										elif realNotePrediction == 4:
											stringPredictions.append('Whole-Note')

										return stringPredictions, testingIn


							# rest 
							elif notePrediction == 2:

								# rest - EIGHTH, QUARTER, WHOLE?
								restPredGraph = Graph()

								with restPredGraph.as_default():

									session6 = Session()
									with session6.as_default():

										#load rest model
										model = load_model("/home/Rhythm/Backend/user/routes/rest_model.h5")

										predictions = model.predict(testingIn)
	
										restPrediction = np.argmax(predictions[i])
										print("Rest Prediction", predictions)

										if restPrediction == 0:
											stringPredictions.append('Eighth-Rest')
										elif restPrediction == 1:
											stringPredictions.append('Quarter-Rest')
										elif restPrediction == 2:
											stringPredictions.append('Whole-Half-Rest')

										return stringPredictions, testingIn



if __name__ == '__main__':

	trainingIn, trainingOut, testingIn, testingOut = getData()

	# trainGeneralNN(trainingIn, trainingOut, testingIn, testingOut)
	# testGeneralNN(testingIn, testingOut)

	# trainClefNN(trainingIn, trainingOut, testingIn, testingOut)
	# testClefNN(testingIn, testingOut)

	# trainNoteNN(trainingIn, trainingOut, testingIn, testingOut)
	# testNoteNN(testingIn, testingOut)

	# trainRealNoteNN(trainingIn, trainingOut, testingIn, testingOut)
	# testRealNoteNN(testingIn, testingOut)

	# trainRestNN(trainingIn, trainingOut, testingIn, testingOut)
	# testRestNN(testingIn, testingOut)

	# trainExtrasNN(trainingIn, trainingOut, testingIn, testingOut)
	# testExtrasNN(testingIn, testingOut)

	# checkPredictions(testingIn, testingOut)
