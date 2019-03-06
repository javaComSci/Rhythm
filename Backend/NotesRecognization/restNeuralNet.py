import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model

model = load_model("rest_model.h5")

def predictRest(testingInput):
	# which rest
	predictions = model.predict(testingInput)

	# actual value of the predictions
	overallPredictions = []

	for i in range(predictions.shape[0]):		
		currentPrediction = np.argmax(predictions[i])
		print("Rest Prediction", predictions)
		overallPredictions.append(currentPrediction)

	return overallPredictions