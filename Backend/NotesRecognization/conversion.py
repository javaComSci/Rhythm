import partition
import neuralNet
import numpy as np
import cv2
import json
import MIDImaker
import json
import sendToCloud

# from .. import MySQL

if __name__ == "__main__":
	file_path = "ExamplePredictions/DATA/s5.jpg"

	mask, SOL, staff_lines = partition.full_partition(file_path)

	ob_counter = 0

	partition.print_objects(mask, SOL, staff_lines, "ExamplePredictions/predictions/")

	exit(1)

	dicty = {"clef":1, "notes":[]}

	cv2.imwrite("ExamplePredictions/predictions/full_img.jpg", mask)


	with open('data.json', 'w') as outfile:

		bigData = {}

		bigData['clef'] = 1
		bigData['notes'] = []

		gclef = False
		cclef = False
		fclef = False

		for i in range(len(SOL)):
			n_arr = partition.SO_to_array(SOL[i])

			print(n_arr.shape)

			flat_arr = n_arr.flatten().reshape((1,3500))


			ob_prediction, im = neuralNet.predict(flat_arr)
			im = im.reshape((70,50)) * 255
			if ob_prediction == None or len(ob_prediction) == 0:
				ob_prediction = "DEFAULT"

			cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction[0]), im)

			data = {}

			clefCount = 0

			print("OB PREDICTION", ob_prediction[0])

			if ob_prediction[0] == 'GClef':
				SOL[i].clef = 1
				data['note'] = 0
				data['pitch'] = 1
				data['length'] = 0
				gclef = True
			elif ob_prediction[0] == 'CClef':
				SOL[i].clef = 2
				data['note'] = 6
				data['pitch'] = 1
				data['length'] = 0
				cclef = True
			elif ob_prediction[0] == 'FClef':
				SOL[i].clef = 3
				data['note'] = 7
				data['pitch'] = 1
				data['length'] = 0
				fclef = True
			elif ob_prediction[0] == 'Sixteenth-Note':
				SOL[i].duration = .125
				data['note'] = 5
				data['pitch'] = SOL[i].run
				data['length'] = .125
			elif ob_prediction[0] == 'Eighth-Note':
				SOL[i].duration = .5
				data['note'] = 1
				data['pitch'] = SOL[i].run
				data['length'] = .5
			elif ob_prediction[0] == 'Quarter-Note':
				SOL[i].duration = 1
				data['note'] = 2
				data['pitch'] = SOL[i].run
				data['length'] = 1
			elif ob_prediction[0] == 'Half-Note':
				SOL[i].durationn = 2
				data['note'] = 3
				data['pitch'] = SOL[i].run
				data['length'] = 2
			elif ob_prediction[0] == 'Whole-Note':
				SOL[i].duration = 4
				data['note'] = 8
				data['pitch'] = SOL[i].run
				data['length'] = 4
			elif ob_prediction[0] == 'Eighth-Rest':
				SOL[i].rest = .5
				data['note'] = 9
				data['pitch'] = SOL[i].run
				data['length'] = .5
			elif ob_prediction[0] == 'Quarter-Rest':
				SOL[i].rest = 1
				data['note'] = 10
				data['pitch'] = SOL[i].run
				data['length'] = 1
			elif ob_prediction[0] == 'Whole-Half-Rest':
				SOL[i].rest = 2
				data['note'] = 11
				data['pitch'] = SOL[i].run
				data['length'] = 2
			elif ob_prediction[0] == 'Sharp':
				SOL[i].accidental = 1
				data['note'] = 13
				data['pitch'] = SOL[i].run
				data['length'] = 0
			elif ob_prediction[0] == 'Flat':
				SOL[i].accidental = 2
				data['note'] = 14
				data['pitch'] = SOL[i].run
				data['length'] = 0

			print(SOL[i].duration, SOL[i].accidental)

			ob_counter += 1

			bigData['notes'].append(data)

			print("NOTES", bigData["notes"])

			print("DATA", data)

		if gclef == True and fclef == True:
			bigData['clef'] = 1
		elif gclef == True:
			bigData['clef'] = 0
		elif fclef == True:
			bigData['clef'] = 2
		elif cclef == True:
			bigData['clef'] = 3

		print("BIG DATA", bigData)

		jsonData = json.dumps(bigData)

		print("bigData")
		print(bigData)

		with open('data.txt', 'w') as outfile:  
			json.dump(jsonData, outfile)

		sendToCloud.cloud(jsonData)

	MF = MIDImaker.MIDIob(SOL)
	filey = MF.convert_to_MIDI()





