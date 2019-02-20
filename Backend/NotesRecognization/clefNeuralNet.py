import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model

model = load_model("clef_model.h5")

def predictClef(testingInput):
	# which clef
	predictions = model.predict(testingInput)

	# actual value of the predictions
	overallPredictions = []

	for i in range(predictions.shape[0]):		
		currentPrediction = np.argmax(predictions[i])
		print("AAA", predictions, predictions.shape)
		print("ALL THE PREDICTIONS", predictions[i], predictions[i].shape)
		overallPredictions.append(currentPrediction)

	return overallPredictions