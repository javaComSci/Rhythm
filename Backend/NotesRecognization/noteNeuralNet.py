import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import load_model
from tensorflow import Graph, Session

def predictNote(testingInput):
	return 5
	print("G1")
	notePredGraph = Graph()

	with notePredGraph.as_default():
		print("G2")
		session = Session()
		with session.as_default():
			#load model
			model = load_model("notes_model.h5")

			predictions = model.predict(testingInput)

			# actual value of the predictions
			overallPredictions = []

			for i in range(predictions.shape[0]):		
				currentPrediction = np.argmax(predictions[i])
				print("Note Prediction", predictions)
				overallPredictions.append(currentPrediction)

			return overallPredictions