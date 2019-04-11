import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model
from tensorflow import Graph, Session

def predictExtraNote(testingInput):
	extrasPredGraph = Graph()

	with extrasPredGraph.as_default():
		session = Session()
		with session.as_default():
			#load model
			model = load_model("extras_model.h5")

			predictions = model.predict(testingInput)

			# actual value of the predictions
			overallPredictions = []

			for i in range(predictions.shape[0]):		
				currentPrediction = np.argmax(predictions[i])
				print("Extras Prediction", predictions)
				overallPredictions.append(currentPrediction)

			return overallPredictions