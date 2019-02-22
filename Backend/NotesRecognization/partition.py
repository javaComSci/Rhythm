import cv2
import numpy as np

#allows creating individual objects found on a piece of sheet music
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

# @image - 2d numpy array
# @return - list of rows that contain run blocks
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

# @image - 2d numpy array
# @runs - list of row locations for runs
# @return - void
#	Removes runs from image while attempting to skip over neighboring objects
def remove_runs_and_fill(image, runs):
	for row in runs:
		for col in range(image.shape[1]):
			if row > 0 and image[row-1][col] == 255:
				image[row][col] = 255

# @image - 2d numpy array
# @return - list of columns that contain vertical dividers
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
			if pixel_sum / (image.shape[0] * 1.00) >= 0.1:
				if col not in dividers:
					dividers.append(col)

	return dividers

# @image - 2d numpy array
# @dividers - list of column indices
# @return - void
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

# @image - image of sheet music, preprocessed into binary with runs and dividers removed
# @return - 2D mask of all sheet objects and a list of sheet objects
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

	#merge touching objects that were mis-labeled in the first object location iteration
	merge_touching_objects(mask, sheet_object_list)

	#prunes objects that dont meet criteria out of SOL
	prune_objects(mask, sheet_object_list)

	#Return mask with objects labels and list of each individual object
	return mask, sheet_object_list

# @image - image of binary preprocessed sheet music
# @mask - Contains labels for which pixels correspond to which objects
# @row - row of unlabeled pixel
# @col - column of unlabeled pixel
# @return - int representing object label
#	Scans around unlabeled pixel to attempt to determine pixel object label
def scan_unidentified_pixel(image,mask,row,col):
	#Initialize the row and column you will start/end scanning from
	startRow = max(row-2,0)
	startCol = max(col-2,0)
	endRow = min(image.shape[0], row+2)
	endCol = min(image.shape[1], col+3)

	#For all pixels in scan range around unlabeled pixel
	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			#If pixel is not the unlabeled pixel, and it is labeled in the mask
			if (i != row or j != col) and mask[i][j] != 0:
				#Return object number noted in the mask
				return mask[i][j]

	#If no mask values were found, return -1, indicating this is a new object
	return -1

# @mask - Contains labels for identifying which pixels belong to which objects
# @row - row of the labeled pixel
# @col - col of the labeled pixel
# @return - 2 integers representing what object the given pixel is touching
#	Scans around an identified pixel to determine if it is touching another object
def scan_identified_pixel(mask,row,col):
	#intialize the start and ending rows to be scanned
	startRow = max(row-2,0)
	startCol = max(col-2,0)
	endRow = min(mask.shape[0], row+2)
	endCol = min(mask.shape[1], col+2)

	#label of current pixel
	o1 = mask[row][col]

	#check bounds around o1
	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			#If found a different object label, return both labels
			if mask[i][j] != 0 and mask[i][j] != o1:
				return o1, mask[i][j]

	return o1, o1

# @o1_label - label of object in mask
# @o2_labels - label of object in mask
# @mask - Contains labels for identifying which pixels belong to which objects
# @SOL - List of all objects on the music sheet
# @return - void
# 	Given the object labels for two objects present in the SOL, merge both objects into one
#	and update the corresponding mask values and SOL entries
def merge_sheet_objects(o1_label,o2_label,mask,SOL):

	#Find index for each boject label
	ob1 = locate_sheet_object_index(o1_label,SOL)
	ob2 = locate_sheet_object_index(o2_label,SOL)

	#add pixels from SOL[ob2] to SOL[ob1]'s pixel_list
	SOL[ob1].pixel_list = SOL[ob1].pixel_list + SOL[ob2].pixel_list

	#update the image bounds for SOL[ob1}
	SOL[ob1].update_bounds()

	#update the mask, replace SL[ob2] pixels with o1_label
	update_mask(mask,SOL[ob2],SOL[ob1].object_number)

	#remove SOL[ob2] from the list of objects
	del SOL[ob2]

# @mask - Contains labels for identifying which pixels belong to which objects
# @sheet_object - A single object found on the music sheet
# @new_label - The label to replace all values of sheet_object's pixel in the mask
# @return - void
#	Replaces all entries of a single sheet object with the labels of another sheet object
def update_mask(mask, sheet_object, new_label):

	for p in sheet_object.pixel_list:

		#replace pixel value in mask with new label
		mask[p[0]][p[1]] = new_label

# @label - object label to be located
# @SOL - List of sheet objects found on the music sheet
# @return - index in SOL of sheet object with provided label
#	Finds the index of a given sheet object in the SOL
def locate_sheet_object_index(label, SOL):
	for i in range(len(SOL)):

		#if object number matches provided label, return i
		if SOL[i].object_number == label:
			return i

	#No such label present in SOL
	return -1

# @mask - Contains labels for identifying which pixels belong to which objects
# @SOL - List of sheet objects found on the music sheet
# @return - void
#	Finds all touching objects in the mask, and merges them into single objects
def merge_touching_objects(mask,SOL):

	#for every pixel in mask
	for row in range(mask.shape[0]):
		for col in range(mask.shape[1]):
			if mask[row][col] != 0:

				#scan around mask[row][col] to see if is touching a different object
				o1,o2 = scan_identified_pixel(mask,row,col)
				
				#if o1 != o2, touching objects have been located
				if o1 != o2:

					#merge touching objects
					merge_sheet_objects(o1,o2,mask,SOL)

# @ob - A single sheet object
# @return - True if width is too small, false otherwise
#	checks the width of an object, returning true if it is too small
def check_width(ob):
	if ob.C2 - ob.C1 <= 5:
		return True
	return False

# @ob - A single sheet object
# @return - True if height is too small, false otherwise
#	checks the height of an object, returning true if it is too small
def check_height(ob):
	if ob.R2 - ob.R1 <= 5:
		return True
	return False

# @ob - A single sheet object
# @return - True if area is too small, false otherwise
#	checks the area of an object, returning true if it is too small
def check_area(ob):
	if len(ob.pixel_list) <= 35:
		return True
	return False

# @ob - A single sheet object
# @return - True if area is too many pixels in image are of the object, false otherwise
#	checks the pixel area of an object, returning true if it is too large
def check_object_area(ob):
	if len(ob.pixel_list) / (1.00 * (ob.R2 - ob.R1) * (ob.C2 - ob.C1)) >= 0.8:
		return True
	return False

# @mask - Contains labels for identifying which pixels belong to which objects
# @SOL - List of sheet list objects
# @return - void
#	prunes out objects that dont meet specific criteria in an image
def prune_objects(mask, SOL):
	ob = 0
	while ob < len(SOL):

		#if the object isn't wide, tall, or sized large enough
		prune = check_width(SOL[ob]) or check_height(SOL[ob]) or check_area(SOL[ob]) or check_object_area(SOL[ob])

		if prune:

			#update mask with removed object
			update_mask(mask,SOL[ob],0)

			#delete object from SOL
			del SOL[ob]
		else:
			ob += 1

# @mask - Contains labels for identifying which pixels belong to which objects
# @SOL - List of sheet list objects
# @path - path that jpgs will be written to
# @return - void
#	Prints all objects in sheet object list as jpgs
def print_objects(mask,SOL,path=""):
	#Ensures path is in correct format
	if path.endswith("/") == False:
		path = path + "/"

	full_img = np.zeros(mask.shape)

	#for every object in sheet object list
	for ob in SOL:
		#Creates new cropped imag that will be filled with a single object
		new_img = np.zeros((ob.R2-ob.R1+1,ob.C2-ob.C1+1))

		#For each pixel in the object, place the pixel into new_img
		for tup in ob.pixel_list:
			full_img[tup[0]][tup[1]] = 255
			new_img[tup[0] - ob.R1][tup[1] - ob.C1] = 255

		#Write object to specified path
		cv2.imwrite("{}ob_{}.jpg".format(path,ob.object_number), new_img)

	#Write full object image to specified path
	cv2.imwrite("{}FullImage.jpg".format(path), full_img)

# @ob - A single sheet object
# @return - 2D numpy array of sheet object
#	Converts a sheet object into it's corresponding numpy array
def SO_to_array(ob):
	#intitialize array
	n_arr = np.ones((70,50))

	#set flag of image size
	flag = False

	#If sheet object cant fit into a 70x50 array, create minimum sized array that works
	if (ob.R2 - ob.R1 >= 70 or ob.C2 - ob.C1 >= 50):
		flag = True
		n_arr = np.ones(((ob.R2 - ob.R1 + 1),(ob.C2 - ob.C1 + 1)))

	#For every pixel in the sheet object
	for p in ob.pixel_list:

		#Center pixels
		Rcenter = int((70 - (ob.R2 - ob.R1))/2.00)
		Ccenter = int((50 - (ob.C2 - ob.C1))/2.00)

		#Set centering to 0 if using custom array size
		if flag or Rcenter < 0:
			Rcenter = 0

		if flag or Ccenter < 0:
			Ccenter = 0

		#Set pixel value to black in corresponding pixel
		n_arr[p[0] - ob.R1 + Rcenter][p[1] - ob.C1 + Ccenter] = 0
		
	#Resize array to 70x50 if it was a custom size array
	if flag:
		n_arr = cv2.resize(n_arr, (70, 50)) 

	return n_arr

# @path - path to music sheet jpg
# @return - 2d mask array, and a list of the sheet objects
#	fully performs tha object partion steps, returning the mask of the objects and the 
#	list of the objects
def full_partition(path):
	#load image as grayscale
	im_gray =  cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	#convert image to binary
	(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	#print "Completed 'image load'"

	#resize image if it is too large
	if (im_bw.shape[0] > 2000 and im_bw.shape[1] > 2000):
		im_bw = cv2.resize(im_bw, (1500, 1500)) 

	#locate runs in the image
	runs = locate_run_blocks(im_bw)

	#remove runs in the image
	remove_runs_and_fill(im_bw, runs)
	#print "Completed 'run segmenting'"

	#locate dividers in the image
	dividers = locate_vertical_dividers(im_bw)

	#remove dividers in the image
	remove_vertical_dividers_and_fill(im_bw, dividers)
	#print "Completed 'divider segmenting'"

	#locate objects in the image
	mask, SOL = locate_objects(im_bw)
	#print "Completed 'object location'"

	return mask, SOL

if __name__ == "__main__":
	mask, SOL = full_partition("DATA/test14.jpg")
	print_objects(mask,SOL,path="test")



