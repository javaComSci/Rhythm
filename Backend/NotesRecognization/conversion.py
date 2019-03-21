import partition
import neuralNet
import numpy as np
import cv2
import json

class JCpenny:
	def __init__(self,note,length,pitch):
		self.note = 1
		self.length = 1
		self.pitch = pitch

if __name__ == "__main__":
	file_path = "ExamplePredictions/DATA/file19.jpg"

	mask, SOL, staff_lines = partition.full_partition(file_path)

	ob_counter = 0

	partition.print_objects(mask, SOL, staff_lines, "ExamplePredictions/predictions/")

	dicty = {"clef":1, "notes":[]}

	cv2.imwrite("ExamplePredictions/predictions/full_img.jpg", mask)


	with open('data.json', 'w') as outfile:
		for ob in SOL:
			n_arr = partition.SO_to_array(ob)

			print(n_arr.shape)

			flat_arr = n_arr.flatten().reshape((1,3500))


			ob_prediction, im = neuralNet.predict(flat_arr)
			im = im.reshape((70,50)) * 255
			if ob_prediction == None or len(ob_prediction) == 0:
				ob_prediction = "DEFAULT"

			cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction[0]), im)

			if ob_prediction == 'G-Clef':
				ob.clef = 1
			elif ob_prediction == 'C-Clef':
				ob.clef = 2
			elif ob_prediction == 'F-Clef':
				ob.clef = 3
			elif ob_prediction == 'Sixteenth Note':
				ob.duration = .0625
			elif ob_prediction == 'Eighth Note':
				ob.duration = .125
			elif ob_prediction == 'Quarter Note':
				ob.duration = .25
			elif ob_prediction == 'Half Note':
				ob.duration = .5
			elif ob_prediction == 'Whole Note':
				ob.duration = 1
			elif ob_prediction == 'Eighth Rest':
				ob.rest = .125
			elif ob_prediction == 'Quarter Rest':
				ob.rest = .25
			elif ob_prediction == 'Half Rest':
				ob.rest = .5
			elif ob_prediction == 'Sharp':
				ob.accidental = 1
			elif ob_prediction == 'Flat':
				ob.accidental = 2

			ob_counter += 1
	print("Number of objects", ob_counter)

