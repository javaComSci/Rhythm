import cv2
import numpy as np
import gc
import time

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

		#run and staff line object is attached to
		self.run = -1 #which row the object is on
		self.staff_line = -1 #which measure the object is on
		self.duration = -1 #duration of the note
		self.clef = -1 #if the object is a clef
		self.rest = -1 #if the object is a rest
		self.accidental = -1 #if the object is a sharp

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
	def update_bounds(self, ob):
		#for every pixel in list, check to see if bounds have changed
		if ob.R1 < self.R1:
			self.R1 = ob.R1
		if ob.R2 > self.R2:
			self.R2 = ob.R2
		if ob.C1 < self.C1:
			self.C1 = ob.C1
		if ob.C2 > self.C2:
			self.C2 = ob.C2

	def remove_pixel(self, tup):
		self.pixel_list.remove(tup)


# @image - 2d numpy array
# @return - list of rows that contain run blocks
#	return a list of rows that have runs in them
def locate_run_blocks(image):
	runs = set()

	imr = image.shape[0]
	imc = image.shape[1]

	#For evert row in the image
	for row in range(imr):

		minRow = max(0, row-1)
		maxRow = min(row+1,imr-1)
		currRow = row

		#Checks total number of pixels found in a given stretch of a row
		pixel_sum = 0

		#If that last seen pixel was an object
		black_flag = False

		#For every column in the image
		for col in range(imc):
			#print(type(image[currRow,col]))
			#If the pixel is black, increase pixel sum if last pixel was black, otherwise set flag
			if not int(image[currRow,col]) or not int(image[maxRow,col]) or not int(image[minRow,col]):
				pixel_sum += 1
			else:
				#If the pixel sum is greater than 10% of the image length, consider it a run
			# and add it to a list of rows to be removed
				if pixel_sum / (imc * 1.00) >= 0.1:
					runs.add(row)
					runs.add(minRow)
					runs.add(maxRow)
				pixel_sum = 0
				black_flag = False


				# if row not in runs:
				# 	runs.append(row)
				# if minRow not in runs:
				# 	runs.append(minRow)
				# if maxRow not in runs:
				# 	runs.append(maxRow)
	return list(runs)

# @image - 2d numpy array
# @runs - list of row locations for runs
# @return - void
#	Removes runs from image while attempting to skip over neighboring objects
def remove_runs_and_fill(image, runs):
	for row in runs:
		for col in range(image.shape[1]):
			if row > 0 and image[row-1,col] == 255:
				image[row][col] = 255

# @image - 2d numpy array
# @return - list of columns that contain vertical dividers
#	returns a list of the columns that contain vertical dividers in the image
def locate_vertical_dividers(image):
	runs = set()

	imr = image.shape[0]
	imc = image.shape[1]

	#For evert row in the image
	for col in range(imc):

		minCol = max(0, col-1)
		maxCol = min(col+1,imc-1)
		currCol = col

		#Checks total number of pixels found in a given stretch of a row
		pixel_sum = 0

		#If that last seen pixel was an object
		black_flag = False

		#For every column in the image
		for row in range(imr):
			#print(type(image[currRow,col]))
			#If the pixel is black, increase pixel sum if last pixel was black, otherwise set flag
			if not int(image[row,currCol]) or not int(image[row,maxCol]) or not int(image[row,minCol]):
				pixel_sum += 1
			else:
				#If the pixel sum is greater than 10% of the image length, consider it a run
			# and add it to a list of rows to be removed
				if pixel_sum / (imc * 1.00) >= 0.1:
					runs.add(col)
					runs.add(minCol)
					runs.add(maxCol)

				pixel_sum = 0
				black_flag = False


				# if row not in runs:
				# 	runs.append(row)
				# if minRow not in runs:
				# 	runs.append(minRow)
				# if maxRow not in runs:
				# 	runs.append(maxRow)
	return list(runs)

# @image - 2d numpy array
# @dividers - list of column indices
# @return - void
#	Removes vertical dividers from image while attempting to ignore neighboring objects
def remove_vertical_dividers_and_fill(image, dividers):
	#For every column in dividers, remove column if pixel to left of black pixel isn't black
	for col in dividers:
		for row in range(image.shape[0]):
			if col > 0 and image[row,col-1] == 255:
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

	if image[row,col] == 255 or mask[row][col] != 0:
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
			if not image[row,col]:
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
			if (i != row or j != col) and mask[i,j] != 0:
				#Return object number noted in the mask
				return mask[i,j]

	#If no mask values were found, return -1, indicating this is a new object
	return -1

# @mask - Contains labels for identifying which pixels belong to which objects
# @row - row of the labeled pixel
# @col - col of the labeled pixel
# @return - 2 integers representing what object the given pixel is touching
#	Scans around an identified pixel to determine if it is touching another object
def scan_identified_pixel(mask,row,col):
	#intialize the start and ending rows to be scanned
	startRow = max(row-3,0)
	startCol = max(col-3,0)
	endRow = min(mask.shape[0], row+3)
	endCol = min(mask.shape[1], col+3)

	#label of current pixel
	o1 = mask[row,col]

	#check bounds around o1
	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			#If found a different object label, return both labels
			if mask[i,j] != 0 and mask[i,j] != o1:
				return o1, mask[i,j]

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
	SOL[ob1].update_bounds(SOL[ob2])

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
			if mask[row,col] != 0:

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
	ar = len(ob.pixel_list) / (1.00 * (ob.R2 - ob.R1) * (ob.C2 - ob.C1))
	if ar >= 0.8:
		return True

	# ar1 = len(ob.pixel_list) / ((1.00 * 3500))
	# if ar1 <= 0.1:
	# 	return True
	return False

def check_center(ob):
	ob_arr = SO_to_array(ob)

	min_row = max(0,int(ob_arr.shape[0]/2)-3)
	max_row = min(ob_arr.shape[0], int(ob_arr.shape[0]/2)+4)

	for i in range(min_row, max_row):
		for j in range(ob_arr.shape[1]):
			if ob_arr[i][j] == 0:
				return False

	return True

def check_edges(ob):
	ob_arr = SO_to_array(ob)

	min_top = 0
	max_top = min(ob_arr.shape[0], 5)

	for i in range(min_top, max_top):
		for j in range(ob_arr.shape[1]):
			if ob_arr[i][j] == 0:
				return False

	min_bot = max(0,ob_arr.shape[0]-5)
	max_bot = ob_arr.shape[0]

	for i in range(min_bot, max_bot):
		for j in range(ob_arr.shape[1]):
			if ob_arr[i][j] == 0:
				return False

	return True



# @mask - Contains labels for identifying which pixels belong to which objects
# @SOL - List of sheet list objects
# @return - void
#	prunes out objects that dont meet specific criteria in an image
def prune_objects(mask, SOL):
	ob = 0
	while ob < len(SOL):

		#if the object isn't wide, tall, or sized large enough
		cw = check_width(SOL[ob])
		ch = check_height(SOL[ob])
		ca = check_area(SOL[ob])
		coa = check_object_area(SOL[ob])
		cc = check_center(SOL[ob])
		ce = check_edges(SOL[ob])
		prune =  cw or ch or ca or coa or cc or ce
		if prune:
			cv2.imwrite("{}{}ob_{}{}{}{}.jpg".format("ExamplePredictions/prunePredictions/",SOL[ob].R1,cw,ch,ca,coa), SO_to_array(SOL[ob]))

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
def print_objects(shape,SOL,sl,path="",staff_lines=False):
	#Ensures path is in correct format
	if path.endswith("/") == False:
		path = path + "/"

	full_img = np.zeros(shape)
	county = 0

	#for every object in sheet object list
	for ob in SOL:
		#Creates new cropped imag that will be filled with a single object
		#new_img = np.zeros((ob.R2-ob.R1+1,ob.C2-ob.C1+1))

		#For each pixel in the object, place the pixel into new_img
		for tup in ob.pixel_list:
			#update full image
			full_img[tup[0]][tup[1]] = 255
			#update object image
			#new_img[tup[0] - ob.R1][tup[1] - ob.C1] = 255

		new_img = SO_to_array(ob)

		#Write object to specified path
		cv2.imwrite("{}{}ob_{}_R{}SL{}.jpg".format(path,county,ob.object_number,ob.run,ob.staff_line), new_img)

		county += 1
	if staff_lines:
		for s in sl:
			for r in s:
				for c in range(full_img.shape[1]):
					if r < full_img.shape[0]:
						full_img[r][c] = 255

	#Write full object image to specified path
	cv2.imwrite("{}FullImage.jpg".format(path), full_img)

# @ob - A single sheet object
# @return - 2D numpy array of sheet object
#	Converts a sheet object into it's corresponding numpy array
def SO_to_array(ob, resize=True):
	#intitialize array
	n_arr = np.ones((70,50))*255

	#set flag of image size
	flag = False

	shift = 0

	#If sheet object cant fit into a 70x50 array, create minimum sized array that works
	if not resize or (ob.R2 - ob.R1 >= 70 or ob.C2 - ob.C1 >= 50):
		flag = True

		if resize:
			shift = int((70/50) * (ob.C2 - ob.C1 + 1) - (ob.R2 - ob.R1 + 1))

		if shift < 1:
			shift = 0

		n_arr = np.ones(((shift + ob.R2 - ob.R1 + 1),(ob.C2 - ob.C1 + 1))) * 255

	#For every pixel in the sheet object
	for p in ob.pixel_list:

		#Center pixels
		Rcenter = int((70 - (shift + ob.R2 - ob.R1))/2.00)
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
		n_arr = cv2.resize(n_arr, (50, 70))

	return n_arr

# @path - path to music sheet jpg
# @return - 2d mask array, and a list of the sheet objects
#	fully performs tha object partion steps, returning the mask of the objects and the
#	list of the objects
def full_partition(path, x=0, y=0, b_height=0, b_width=0):
	#load image as grayscale
	print("BEFORE LOAD")
	im_gray =  cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	#cv2.imwrite("{}starter.jpg".format(path), im_gray)

	if (type(im_gray) == None):
		print("IN THE EXCEPTION")
		raise Exception("IMAGE LOAD FAIL")
		return

	print("AFTER")
	#convert image to binary
	(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	#print "Completed 'image load'"

	# print("pre rotate abount to print")

	# cv2.imwrite("/home/Rhythm/Backend/user/routes/pre_rotate.jpg", im_bw)


	# if (im_bw.shape[0] < im_bw.shape[1]):
	# 	im_bw = rotate_scale(im_bw, int(b_height), int(b_width), int(x), int(y), r=True)
	# else:
	# 	im_bw = rotate_scale(im_bw,int(b_height), int(b_width), int(x), int(y), r=False)

	# print("post rotate abount to print")

	# cv2.imwrite("/home/Rhythm/Backend/user/routes/post_rotate.jpg", im_bw)

	# print('completed image rotate and write')

	#cv2.imwrite("{}FullImage_binary.jpg".format(path), im_bw)

	#resize image if it is too large
	# if (im_bw.shape[0] > 2000 and im_bw.shape[1] > 2000):
	# 	im_bw = cv2.resize(im_bw, (1500, 1500))

	#start_time_1 = time.time() ##
	#locate runs in the image
	#start_time = time.time()
	runs = locate_run_blocks(im_bw)
	#print("11_Time: {}".format(time.time() - start_time))

	#start_time = time.time()
	#merge runs into pruned format
	pruned_runs = prune_runs(runs)
	#print("12_Time: {}".format(time.time() - start_time))


	#start_time = time.time()
	#group runs by measures, add in-between rows for runs
	staff_lines = augment_runs(pruned_runs)
	#print("13_Time: {}".format(time.time() - start_time))
	# del pruned_runs
	# gc.collect()

	#print "Completed 'run segmenting'"

	#start_time = time.time()
	#locate dividers in the image
	dividers = locate_vertical_dividers(im_bw)
	#print("14_Time: {}".format(time.time() - start_time))

	#start_time = time.time()
	#remove dividers in the image
	remove_vertical_dividers_and_fill(im_bw, dividers)
	#print("15_Time: {}".format(time.time() - start_time))

	#start_time = time.time()
	#remove runs in the image
	remove_runs_and_fill(im_bw, runs)
	#print("16_Time: {}".format(time.time() - start_time))

	#print("1_Time: {}".format(time.time() - start_time_1))
	# del runs
	# del dividers
	# gc.collect()
	#print "Completed 'divider segmenting'"

	#start_time = time.time()
	#Thickens the iamge around black pixels
	thick_mask = thickener(im_bw)

	#start_time = time.time()
	#locate objects in the image
	mask, SOL = locate_objects(thick_mask)

	#print("2_Time: {}".format(time.time() - start_time))

	# del thick_mask
	# gc.collect()

	#start_time = time.time()
	mask, SOL = de_thicken(mask,SOL,im_bw)

	#print("3_Time: {}".format(time.time() - start_time))
	#print "Completed 'object location'"
	# del im_bw
	# gc.collect()

	#start_time = time.time()
	#locate row and staff lines
	locate_note_run(SOL, staff_lines)

	#print("4_Time: {}".format(time.time() - start_time))

	#start_time = time.time()
	#sort SOL
	sort_SOL(SOL)

	print('almost done with the ol-partitionator 5000')
	#print("5_Time: {}".format(time.time() - start_time))

	img_shape = mask.shape

	# del mask
	# gc.collect()

	return SOL, img_shape, staff_lines

#@ im_bw - A binary image
#@ return - A binary image where black pixels have been expanded
#	Returns an image that has each black pixel expanded into 9 pixels, making lines thicler
#	and more defined
def thickener(im_bw):
	thick_mask = np.ones(im_bw.shape)*255

	for row in range(im_bw.shape[0]):
		for col in range(im_bw.shape[1]):
			if im_bw[row,col] == 0:
				expand_pixel(thick_mask, row, col)

	return thick_mask

def de_thicken(mask, SOL, im_bw):
	for ob in SOL:
		for p in ob.pixel_list:
			if im_bw[p[0],p[1]] == 255:
				mask[p[0]][p[1]] = 0
				ob.remove_pixel(p)

	return mask, SOL

#@ mask - mask to have expanded pixels added to
#@ row - row of current pixel
#@ col - col of current pixel
#@ return - None
#	Given a row and col, put black pixels at each of the surrounding indices
def expand_pixel(mask, row, col):
	startRow = max(row-1,0)
	startCol = max(col-1,0)
	endRow = min(mask.shape[0], row+2)
	endCol = min(mask.shape[1], col+2)

	for r in range(startRow,endRow):
		for c in range(startCol, endCol):
			mask[r][c] = 0


#@ pr - a list of pruned runs
#@ return - a list of all the staff lines and the rows that are present in the staff lines
#	Adds middle rows to a list of the 5 runs in a single staff line. Places runs in their correct
#	staff lines
def augment_runs(pr):
	#intitialize staff_lines array
	staff_lines = []

	#remove extra rows if entire measure was not in image
	pr = pr[:len(pr) - (len(pr) % 5)]

	#group runs by sets of 5 into staff_lines, creating staff lines
	for m in range(0,len(pr),5):
		staff_lines.append(pr[m:m+5])

	#for every staff line in staff_lines
	for sl in range(len(staff_lines)):
		#calculate average run distance for a given staff line
		avg_dist = average_run_distance(staff_lines[sl])

		#add row at front and end of list of runs
		staff_lines[sl].insert(0,staff_lines[sl][0] - avg_dist)
		staff_lines[sl].append(staff_lines[sl][len(staff_lines[sl]) - 1] + avg_dist)

		#add rows between each previous row of staff line
		list_len = len(staff_lines[sl])
		for d in range(1, list_len):
			# value of new row
			val = staff_lines[sl][2*d - 2] + int(avg_dist/2)
			#insert new row between other two rows
			staff_lines[sl].insert(2*d - 1,val)

	return staff_lines

#@ run_list - a list of rows
#@ return - The avg distance between each row
def average_run_distance(run_list):
	#initialize avgs
	avg = 0

	#sum all differences between averages
	for i in range(len(run_list)-1):
		avg += abs(run_list[i+1] - run_list[i])

	num = max(2, len(run_list))
	#divide by number of differences
	avg = float(avg) / (num-1)

	return int(avg)

#@ runs - list of all the rows that may contain a run
#@ return - a list of merged runs
#	Given a list of runs, they will be merged into their close counterparts to
#	create a list of the true runs that make up the music sheet
def prune_runs(runs):
	pruned = []

	new_set = []

	#for every run
	for r in runs:
		#if new set is empty, add the run
		if len(new_set) == 0:
			new_set.append(r)
		# if the current run is within 1 pixel of the previous run add it set
		elif abs(new_set[len(new_set) - 1] - r) <= 2:
			new_set.append(r)
		#add new set as it's own singular run
		else:
			pruned.append(new_set)
			new_set = []

	#append final set
	pruned.append(new_set)

	final_runs = []

	num = max(1, len(s))
	#find average of all rows in each run
	for s in pruned:
		final_runs.append(int(float(sum(s))/num))

	return final_runs

#@ SOL - list of sheet objects
#@ runs - list of runs found in music sheet
#@ return - void
#	Sets the predicted run/staff_line for each note
def locate_note_run(SOL,staff_lines):
	for ob in SOL:
		#get object in array form
		ob_arr = SO_to_array(ob, resize=False)

		#figure out if object is top or bottom heavy
		note_weight = top_bottom_heavy(ob_arr)

		#starting row of object
		expected_row = ob.R1

		if note_weight == 0: #top heavy
			expected_row += ob_arr.shape[0] / 5
		else: #bottom heavy
			expected_row += (ob_arr.shape[0] * 4) / 5

		#find closest row to expected row
		cr, sl = closest_row(expected_row,staff_lines)

		#set which row and staff line object is on
		ob.run = cr
		ob.staff_line = sl

#@ n_arr - a pixel representation of a sheet object
#@ return - 0 if the object is top heavy, 1 otherwise
def top_bottom_heavy(n_arr):
	#get top and bottom half of provided array
	top_half = n_arr[:int(n_arr.shape[0]/2),:]
	bottom_half = n_arr[int(n_arr.shape[0]/2):,:]

	#notes are black pixels, with a value of 0. More white pixels, mean less object space
	if np.sum(top_half) <= np.sum(bottom_half):
		#object is top heavy
		return 0

	#object is bottom heavy
	return 1

#@ er - Expected row for which a note is placed on
#@ measures
#@ retrun - returns measure and row of measure that note occurs on
def closest_row(er, staff_lines):
	#initialize min distance to INF
	dist = float("inf")

	#current closest row
	cr = -1
	mes = -1

	for sl in range(len(staff_lines)):
		#for every row
		for r in range(len(staff_lines[sl])):
			#if distance from expected note row to a given row is less than current min distance
			if abs(staff_lines[sl][r] - er) < dist:
				#update current row
				cr = r
				#update current measure
				mes = sl
				#update min distance
				dist = abs(staff_lines[sl][r] - er)

	return cr, mes

#@ SOL - list of sheet objects
#@ return - None
# Sorts the SOL by notes from top left to bottom right
def sort_SOL(SOL):
	SOL.sort(key = lambda ob: (ob.staff_line, ob.C1))

def rotate_scale(image, bh=0, bw=0, x=0, y=0, r=False):
	if r:
		np.rot90(image, 3)

	start_h = int(image.shape[0] / 20) - 1
	start_w = int(image.shape[1] / 30) - 1

	h = int(image.shape[0] - (3*image.shape[0] / 20))
	w = int(image.shape[1] - (2*image.shape[1] / 30))

	new_img = np.ones((h,w))

	print('original img {}'.format(image.shape))
	print('new img {}'.format(new_img.shape))
	for r in range(h):
		for c in range(w):
			new_img[r][c] = image[start_h + r][start_w + c]

	print (new_img)
	return new_img



if __name__ == "__main__":
	start_time = time.time()
	SOL, shape, sl = full_partition("ExamplePredictions/DATA/s5.jpg")
	print("Total_Time: {}".format(time.time() - start_time))

	print_objects(shape,SOL,sl,path="ExamplePredictions/predictions",staff_lines=False)
