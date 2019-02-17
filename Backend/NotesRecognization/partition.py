import cv2
import numpy as np

class sheet_object:
	def __init__(self,tup,object_number):
		#list of pixel locations
		self.pixel_list = []
		self.pixel_list.append(tup)
		self.object_number = object_number

		#Top and bottom right corners
		self.R1 = self.R2 = tup[0]

		#Top and bottom left corners
		self.C1 = self.C2 = tup[1]

	#tup - (row,column) location of a pixel in specified object
	#	Add pixel to an object
	def add_pixel(self,tup):
		#append new pixel to pixel list
		self.pixel_list.append(tup)

		#Updates pixel bounds of image based on new pixel bounds
		if tup[0] < self.R1:
			self.R1 = tup[0]
		if tup[0] > self.R2:
			self.R2 = tup[0]
		if tup[1] < self.C1:
			self.C1 = tup[1]
		if tup[1] > self.C2:
			self.C2 = tup[1]

	#Update bounds of object
	def update_bounds(self):
		#for every pixel in list, check to see if bounds have changed
		for p in self.pixel_list:
			if p[0] < self.R1:
				self.R1 = p[0]
			if p[0] > self.R2:
				self.R2 = p[0]
			if p[1] < self.C1:
				self.C1 = p[1]
			if p[1] > self.C2:
				self.C2 = p[1]



#image - 2d numpy array
#	return a list of rows that have runs in them
def locate_run_blocks(image):
	runs = []

	#For evert row in the image
	for row in range(image.shape[0]):

		#Checks total number of pixels found in a given stretch of a row
		pixel_sum = 0

		#If that last seen pixel was an object
		black_flag = False

		#For every column in the image
		for col in range(image.shape[1]):

			#If the pixel is black, increase pixel sum if last pixel was black, otherwise set flag
			if image[row][col] == 0:
				if black_flag:
					pixel_sum += 1
				else:
					black_flag = True
					pixel_sum += 1
			else:
				pixel_sum = 0;
				black_flag = False

			#If the pixel sum is greater than 10% of the image length, consider it a run
			# and add it to a list of rows to be removed
			if pixel_sum / (image.shape[1] * 1.00) >= 0.1:
				if row not in runs:
					runs.append(row)

	return runs

#image - 2d numpy array
#runs - list of row locations for rns
#	Removes runs from image while attempting to skip over neighboring objects
def remove_runs_and_fill(image, runs):
	#For every row in runs, remove each black pixel in row if pixel above isnt black
	for row in runs:
		for col in range(image.shape[1]):
			if row > 0 and image[row-1][col] == 255:
				image[row][col] = 255

#image - 2d numpy array
#	returns a list of the columns that contain vertical dividers in the image
def locate_vertical_dividers(image):
	dividers = []

	#For every column in the image
	for col in range(image.shape[1]):

		#Sum of pixels found in a given column stretch
		pixel_sum = 0

		#if Last seen pixel was an object
		black_flag = False

		#For every row in the image
		for row in range(image.shape[0]):

			#If the pixel is black, increase pixel sum if last pixel was black, otherwise set flag
			if image[row][col] == 0:
				if black_flag:
					pixel_sum += 1
				else:
					black_flag = True
					pixel_sum += 1
			else:
				pixel_sum = 0;
				black_flag = False


			#If the pixel sum is greater than 10% of the image length, consider it a run
			# and add it to a list of rows to be removed
			if pixel_sum / (image.shape[0] * 1.00) >= 0.075:
				if col not in dividers:
					dividers.append(col)

	return dividers

#image - 2d numpy array
#dividers - list of column indices
#	Removes vertical dividers from image while attempting to ignore neighboring objects
def remove_vertical_dividers_and_fill(image, dividers):
	#For every column in dividers, remove column if pixel to left of black pixel isn't black
	for col in dividers:
		for row in range(image.shape[0]):
			if col > 0 and image[row][col-1] == 255:
				image[row][col] = 255

#DEPRECATED
#image - 2d array
#	Recursive parent function that locates all objects in an image and returns mask of the objects
def locate_objects_DEP(image):
	mask = np.zeros(image.shape)

	object_count = 0
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			if image[row][col] == 0 and mask[row][col] == 0:
				object_count += 1
				locate_object_recur(image,mask,row,col,object_count)

	return mask

#DEPRECATED
#image - 2d numpy array
#mask - 2d numpy array
#row - row index
#col - column index
#object_count - current object number
#	Helper function which recursively locates all new objects
def locate_object_recur_DEP(image,mask,row,col,object_count):

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

#image - image of sheet music, preprocessed into binary with runs and dividers removed
#	Attempts to locate each individual object in the provided image
def locate_objects(image):

	#Initialize mask and list of sheet objects
	mask = np.zeros(image.shape)
	sheet_object_list = []

	#Count of bojects found
	object_count = 1

	#For eery pixel in the image
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			#If pixel is black
			if image[row][col] == 0:
				#Look for surrounding pixels to see if urrent pixel is part of
				# an already discovered object
				ob_num = scan_unidentified_pixel(image,mask,row,col)

				if ob_num == -1:
					#If object wasnt found, create new object

					#place object number in the mask
					mask[row][col] = object_count

					#Create new sheet object
					tup = (row,col)
					new_obj = sheet_object(tup,object_count)

					#Add sheet object to the list of sheet objects
					sheet_object_list.append(new_obj)

					#Increment total number of found objects
					object_count += 1
				else:
					#Update mask to increase size of already fund object
					mask[row][col] = ob_num

					#Add new object pixel to corresponding object's pixel list
					tup = (row,col)
					sheet_object_list[int(ob_num-1)].add_pixel(tup)

	merge_touching_objects(mask, sheet_object_list)

	#Return mask with objects labels and list of each individual object
	return mask, sheet_object_list

#image - image of binary preprocessed sheet music
#mask - Contains labels for which pixels correspond to which objects
#row - row of unlabeled pixel
#col - column of unlabeled pixel
#	Scans around unlabeled pixel to attempt to determine pixel object label
def scan_unidentified_pixel(image,mask,row,col):
	#Initialize the row and column you will start/end scanning from
	startRow = max(row-1,0)
	startCol = max(col-1,0)
	endRow = min(image.shape[0],row+1)
	endCol = min(image.shape[1], col+1)

	#For all pixels in scan range around unlabeled pixel
	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			#If pixel is not the unlabeled pixel, and it is labeled in the mask
			if (i != row or j != col) and mask[i][j] != 0:
				#Return object number noted in the mask
				return mask[i][j]

	#If no mask values were found, return -1, indicating this is a new object
	return -1

def scan_identified_pixel(mask,row,col):
	startRow = max(row-1,0)
	startCol = max(col-1,0)
	endRow = min(mask.shape[0], row+1)
	endCol = min(mask.shape[1], col+1)

	o1 = mask[row][col]

	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			if mask[i][j] != 0 and mask[i][j] != o1:
				return o1, mask[i][j]

	return o1, o1

def merge_sheet_objects(o1_label,o2_label,mask,SOL):
	ob1 = locate_sheet_object_index(o1_label,SOL)
	ob2 = locate_sheet_object_index(o2_label,SOL)

	SOL[ob1].pixel_list = SOL[ob1].pixel_list + SOL[ob2].pixel_list

	SOL[ob1].update_bounds()

	update_mask(mask,SOL[ob2],SOL[ob1].object_number)

	del SOL[ob2]

def update_mask(mask, sheet_object, new_label):
	for p in sheet_object.pixel_list:
		mask[p[0]][p[1]] = new_label

def locate_sheet_object_index(label, SOL):
	for i in range(len(SOL)):
		if SOL[i].object_number == label:
			return i

	return -1

def merge_touching_objects(mask,SOL):
	for row in range(mask.shape[0]):
		for col in range(mask.shape[1]):
			if mask[row][col] != 0:
				o1,o2 = scan_identified_pixel(mask,row,col)
				if o1 != o2:
					merge_sheet_objects(o1,o2,mask,SOL)

#SOL - List of sheet list objects
#ob_size - size of objects that must be met to meet true-object criteria
#path - path that jpgs will be written to
#	Prints all objects in sheet object list as jpgs
def print_objects(SOL,ob_size=35,path=""):
	#Object idd
	idd = 0

	#Ensures path is in correct format
	if path.endswith("/") == False:
		path = path + "/"

	#for every object in sheet object list
	for ob in SOL:
		if len(ob.pixel_list) >= ob_size:
			#Creates new cropped imag that will be filled with a single object
			new_img = np.zeros((ob.R2-ob.R1+1,ob.C2-ob.C1+1))

			#For each pixel in the object, place the pixel into new_img
			for tup in ob.pixel_list:
				new_img[tup[0] - ob.R1][tup[1] - ob.C1] = 255

			#Write object to specified path
			cv2.imwrite("{}ob_{}.jpg".format(path,idd), new_img)

			#increment naming id
			idd += 1
	



if __name__ == "__main__":
	im_gray = cv2.imread("DATA/test6.jpg", cv2.IMREAD_GRAYSCALE)
	(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	print "Completed 'image load'"

	runs = locate_run_blocks(im_bw)
	remove_runs_and_fill(im_bw, runs)
	print "Completed 'run segmenting'"

	dividers = locate_vertical_dividers(im_bw)
	remove_vertical_dividers_and_fill(im_bw, dividers)
	print "Completed 'divider segmenting'"

	mask, SOL = locate_objects(im_bw)
	print "Completed 'object location'"

	print_objects(SOL,ob_size=45,path="test")
	print "Completed 'print objects'"

	cv2.imshow('image',mask)
	cv2.waitKey(10000)