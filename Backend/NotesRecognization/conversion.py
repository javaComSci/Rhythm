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
	file_path = "ExamplePredictions/DATA/test3.jpg"

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
			ob_counter += 1
	print("Number of objects", ob_counter)
#
# 			print("DIMS", flat_arr.shape)
#
# 			ob_prediction, im = neuralNet.predict(flat_arr)
# 			print("OB PREDICTION", ob_prediction)
# 			im = im.reshape((70,50)) * 255
#
# 			t = 0
#
# 			if ob_prediction == 'G-Clef':
# 				t = 0
# 			elif ob_prediction == 'Eighth Note':
# 				t = 1
# 			elif ob_prediction == 'Quarter Note':
# 				t = 2
# 			elif ob_prediction == 'Half Note':
# 				t = 3
# 			elif ob_prediction == 'Quarter Note':
# 				t = 4
# 			elif ob_prediction == 'Sixteenth Note':
# 				t = 5
# 			elif ob_prediction == 'Whole Note':
# 				t = 6
# 			elif ob_prediction == 'Eighth Rest':
# 				t = 7
# 			elif ob_prediction == 'Quarter Rest':
# 				t = 8
# 			elif ob_prediction == 'Half Rest':
# 				t = 9
# 			elif ob_prediction == 'Sharp':
# 				t = 10
# 			elif ob_prediction == 'Flat':
# 				t = 11
# 			elif ob_prediction == 'C-Clef':
# 				t = 12
# 			elif ob_prediction == 'F-Clef':
# 				t = 13
#
#
# 			cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, t), im)
# 			ob_counter += 1
# 			obby = JCpenny(t,1,ob.run)
# 			print("OBBY", ob.run)
#
# 			dicty["notes"].append(obby.__dict__)
#
# 		json.dump(dicty, outfile)
#
# 	# for ob in SOL:
# 	# 	n_arr = partition.SO_to_array(ob)
#
# 	# 	print(n_arr.shape)
#
# 	# 	flat_arr = n_arr.flatten().reshape((1,3500))
#
# 	# 	print("DIMS", flat_arr.shape)
#
# 	# 	ob_prediction, im = neuralNet.predict(flat_arr)
# 	# 	im = im.reshape((70,50)) * 255
#
# 	# 	cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction[0]), im)
# 	# 	ob_counter += 1
# 	# print("Number of objects", ob_counter)
