import cv2
import numpy as np


#image - 2d numpy array
#	return a list of rows that have runs in them
def locate_run_blocks(image):
	runs = []

	for row in range(image.shape[0]):

		pixel_sum = 0
		black_flag = False
		for col in range(image.shape[1]):

			if image[row][col] == 0:
				if black_flag:
					pixel_sum += 1
				else:
					black_flag = True
			else:
				pixel_sum = 0;
				black_flag = False

			if pixel_sum / (image.shape[1] * 1.00) >= 0.1:
				if row not in runs:
					runs.append(row)

	return runs

#image - 2d numpy array
#runs - list of row locations for rns
#	Removes runs from image while attempting to skip over neighboring objects
def remove_runs_and_fill(image, runs):
	for row in runs:
		for col in range(image.shape[1]):
			if row > 0 and image[row-1][col] == 255:
				image[row][col] = 255

#image - 2d numpy array
#	returns a list of the columns that contain vertical dividers in the image
def locate_vertical_dividers(image):
	dividers = []

	for col in range(image.shape[1]):

		pixel_sum = 0
		black_flag = False
		for row in range(image.shape[0]):

			if image[row][col] == 0:
				if black_flag:
					pixel_sum += 1
				else:
					black_flag = True
			else:
				pixel_sum = 0;
				black_flag = False

			if pixel_sum / (image.shape[0] * 1.00) >= 0.1:
				if col not in dividers:
					dividers.append(col)

	return dividers

#image - 2d numpy array
#dividers - list of column indices
#	Removes vertical dividers from image while attempting to ignore neighboring objects
def remove_vertical_dividers_and_fill(image, dividers):
	for col in dividers:
		for row in range(image.shape[0]):
			if col > 0 and image[row][col-1] == 255:
				image[row][col] = 255

#image - 2d array
#	Recursive parent function that locates all objects in an image and returns mask of the objects
def locate_objects(image):
	mask = np.zeros(image.shape)

	object_count = 0
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			if image[row][col] == 0 and mask[row][col] == 0:
				object_count += 1
				locate_object_recur(image,mask,row,col,object_count)

	return mask

#image - 2d numpy array
#mask - 2d numpy array
#row - row index
#col - column index
#object_count - current object number
#	Helper function which recursively locates all new objects
def locate_object_recur(image,mask,row,col,object_count):

	if image[row][col] == 255 or mask[row][col] != 0:
			return

	mask[row][col] = object_count

	if row+1 < image.shape[0]:
		locate_object_recur(image,mask,row+1,col,object_count)

	if row-1 >= 0:
		locate_object_recur(image,mask,row-1,col,object_count)

	if col+1 < image.shape[1]:
		locate_object_recur(image,mask,row,col+1,object_count)

	if col-1 >= 0:
		locate_object_recur(image,mask,row,col-1,object_count)

im_gray = cv2.imread("DATA/test3.jpg", cv2.IMREAD_GRAYSCALE)
# thresh = 195
# im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


#cv2.imshow('image',im_bw)
#cv2.waitKey(5000)
#resized_image = cv2.resize(im_bw, (1500, 900))
# while im_bw.shape[0] > 750 or im_bw.shape[1] > 750:
# 	im_bw = cv2.resize(im_bw, (0,0), fx=0.50, fy=0.50) 

print(im_bw.shape)


runs = locate_run_blocks(im_bw)
remove_runs_and_fill(im_bw, runs)

dividers = locate_vertical_dividers(im_bw)
remove_vertical_dividers_and_fill(im_bw, dividers)

print runs

resized_image = cv2.resize(im_bw, (700, 700))

mask = locate_objects(resized_image)

print mask[mask != 0]
cv2.imshow('image',mask)
cv2.waitKey(10000)