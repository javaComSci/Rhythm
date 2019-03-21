import partition
import neuralNet
import numpy as np
import cv2
import json
import MIDImaker

class JCpenny:
	def __init__(self,note,length,pitch):
		self.note = 1
		self.length = 1
		self.pitch = pitch

if __name__ == "__main__":
	file_path = "ExamplePredictions/DATA/file7.jpg"

	mask, SOL, staff_lines = partition.full_partition(file_path)

	ob_counter = 0

	partition.print_objects(mask, SOL, staff_lines, "ExamplePredictions/predictions/")

	dicty = {"clef":1, "notes":[]}

	cv2.imwrite("ExamplePredictions/predictions/full_img.jpg", mask)


	with open('data.json', 'w') as outfile:
		for i in range(len(SOL)):
			n_arr = partition.SO_to_array(SOL[i])

			print(n_arr.shape)

			flat_arr = n_arr.flatten().reshape((1,3500))


			ob_prediction, im = neuralNet.predict(flat_arr)
			im = im.reshape((70,50)) * 255
			if ob_prediction == None or len(ob_prediction) == 0:
				ob_prediction = "DEFAULT"

			cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction[0]), im)

			if ob_prediction == 'GClef':
				SOL[i].clef = 1
			elif ob_prediction == 'CClef':
				SOL[i].clef = 2
			elif ob_prediction == 'FClef':
				SOL[i].clef = 3
			elif ob_prediction == 'Sixteenth-Note':
				SOL[i].duration = .0625
			elif ob_prediction == 'Eighth-Note':
				SOL[i].duration = .125
			elif ob_prediction == 'Quarter-Note':
				SOL[i].duration = .25
			elif ob_prediction == 'Half-Note':
				SOL[i].durationn = .5
			elif ob_prediction == 'Whole-Note':
				SOL[i].duration = 1
			elif ob_prediction == 'Eighth-Rest':
				SOL[i].rest = .125
			elif ob_prediction == 'Quarter-Rest':
				SOL[i].rest = .25
			elif ob_prediction == 'Whole-Half-Rest':
				SOL[i].rest = .5
			elif ob_prediction == 'Sharp':
				SOL[i].accidental = 1
			elif ob_prediction == 'Flat':
				SOL[i].accidental = 2

			ob_counter += 1

	MF = MIDImaker.MIDIob(SOL)
	filey = MF.convert_to_MIDI()
	MF.MIDI_to_file(filey, "test.mid")





