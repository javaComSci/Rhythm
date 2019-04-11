import numpy as np
import cv2
import os

if __name__ == "__main__":
	path = './SymbolsUnparsed/Half-Note'
	count = 0

	for (dirpath, dirnames, filenames) in os.walk(path):
		# note type for modification
		for filename in filenames:
				count += 1
				if '.DS_Store' in filename:
					continue

				filepath = os.path.join(path, filename)

				im_gray = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
				(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

				thresh = 127
				im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

				img = np.ones(shape=(im_bw.shape[0],im_bw.shape[1])) * 255

				for i in range(im_bw.shape[0]):
					for j in range(im_bw.shape[1]):
						print(im_bw[i][j])
						if im_bw[i][j] == 0:
							img[i][j] = 0
							if i > 0:
								img[i - 1][j] = 0
							if j > 0:
								img[i][j-1] = 0
							if i < im_bw.shape[0] - 2:
								img[i + 1][j] = 0
							if j < im_bw.shape[1] - 2:
								img[i][j+1] = 0
							if i > 0 and j > 0:
								img[i-1][j-1] = 0
							if i < im_bw.shape[0] - 2 and j < im_bw.shape[1] - 2:
								img[i+1][j+1] = 0

				name = str(count) + '.jpg'

				filepath = os.path.join(path, name)
				print("IMG", img)

				cv2.imwrite(filepath, img)

