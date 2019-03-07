import partition
# import neuralNet
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

	partition.print_objects(mask, SOL, "ExamplePredictions/predictions/")

	# dicty = {"clef":1, "notes":[]}

	# with open('data.json', 'w') as outfile:
	# 	for ob in SOL:
	# 		obby = JCpenny(1,1,ob.run)
	# 		dicty["notes"].append(obby.__dict__)
	# 	json.dump(dicty, outfile)

	for ob in SOL:
		n_arr = partition.SO_to_array(ob)

		print(n_arr.shape)

		flat_arr = n_arr.flatten().reshape((1,3500))

		print("DIMS", flat_arr.shape)

	# 	ob_prediction, im = neuralNet.predict(flat_arr)
	# 	im = im.reshape((70,50)) * 255
	#
	# 	cv2.imwrite("ExamplePredictions/predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction[0]), im)
	# 	ob_counter += 1
	# print("Number of objects", ob_counter)
