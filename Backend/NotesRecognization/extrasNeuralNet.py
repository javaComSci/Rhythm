import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model

model = load_model("extras_model.h5")

def predictExtraNote(testingInput):
	# which extra
	predictions = model.predict(testingInput)

	# actual value of the predictions
	overallPredictions = []

	for i in range(predictions.shape[0]):		
		currentPrediction = np.argmax(predictions[i])
		print("Extra Prediction", predictions)
		overallPredictions.append(currentPrediction)

	return overallPredictions