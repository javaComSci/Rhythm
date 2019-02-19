import partition
import neuralNet
import numpy as np
import cv2

if __name__ == "__main__":
	file_path = "PATH TO JPG"

	mask, SOL = partition.full_partition(file_path)

	ob_counter = 1

	for ob in SOL:
		n_arr = partition.SO_to_array(ob)

		resize_arr = cv2.resize(n_arr, (50, 70))
		flat_arr = np.flatten(n_arr)

		ob_prediction = neuralNet.predict(flat_arr)

		cv2.imwrite("predictions/ob#{}_label:{}.jpg".format(ob_counter, ob_prediction), n_arr)