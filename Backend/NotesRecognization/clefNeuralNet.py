import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model

model = load_model("clef_model.h5")

translations = np.load('translations.npy')
translations = translations.item()
print("TRANLSATIONS", translations)

def predictClef(testingInput):
	# which clef
	predictions = model.predict(testingInput)

	# actual value of the predictions

	# overallPredictions = -np.ones((testingInput.shape[0],1))
	overallPredictions = []

	for i in range(predictions.shape[0]):
		currentPrediction = np.argmax(predictions[i])
		# overallPredictions[i] = translations[currentPrediction]
		overallPredictions.append(translations[currentPrediction])

	return overallPredictions