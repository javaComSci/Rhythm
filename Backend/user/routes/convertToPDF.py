import os
import json
import math
import cv2
import numpy as np

# boundaries for the lines
colLeft = 200
colRight = 4350


def getNotes(fileName):
	file = open(fileName)
	notes = json.load(file)
	file.close()
	return notes


def getNoteType(note, pitch, length):

	noteType = False

	if note == 0 and pitch == 1 and length == 0:
		noteType = 'treble'
	elif note == 6 and pitch == 1 and length == 0:
		noteType = 'alto'
	elif note == 7 and pitch == 1 and length == 0:
		noteType = 'bass'
	elif note == 5 and length == .125:
		noteType = 'sixteenth'
	elif note == 1 and length == .5:
		noteType = 'eighth'
	elif note == 3 and length == 2:
		noteType = 'half'
	elif note == 4 and length == 4:
		noteType = 'whole'
	elif note == 9 and length == .5:
		noteType = 'eighthrest'
	elif note == 10 and length == 1:
		noteType = 'quarterrest'
	elif note == 11 and length == 2:
		noteType = 'halfrest'
	elif note == 12 and length == 4:
		noteType = 'wholerest'
	elif note == 13 and length == 0:
		noteType = 'sharp'
	elif note == 14 and length == 0:
		noteType = 'flat'

	return noteType


def createLines(notes):
	duration = 0

	# find total duration of notes
	for note in notes['notes']:
		duration += note['length']

	duration *= 4

	# find number of measures needed
	measures = int(math.ceil(duration/4))

	# find number of staff lines needed
	staffLines = int(math.ceil(measures/4))

	# total size needed for numpy array, which is A4 size
	notesArr = np.ones((6300, 4550))

	# initial starting point for putting the pixels
	row = 400

	staffLinesStartingPos = []

	# add the lines for the staff lines
	for staffLine in range(staffLines):
		
		print "STAFF LINE"
		print staffLine

		staffLinesStartingPos.append(row)

		# need 5 lines for each row
		for i in range(5):

			print "LINE NUMBER"
			print i

			# for the length of the line
			for j in range(colLeft, colRight):

				# for the thickness of the line with the actual line
				for k in range(row, row + 5):

					notesArr[k][j] = 0

			# to account for the whitespace between the lines
			row = row + 50

		# to account for the white space between staff lines
		row = row + 200


	notesArr = notesArr * 255
	cv2.imwrite("lines.jpg", notesArr)

	return notesArr, staffLinesStartingPos



def placeClefs(notesData, notesArr, staffLinesStartingPos):
	if notesData['clef'] == 1:
		# both clefs, need to alternate

		# convert g clef to numpy arrays and make them with correct size 
		imgTreble = cv2.imread('./assets/gclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgTrebleBW) = cv2.threshold(imgTreble, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgTrebleResized = cv2.resize(imgTrebleBW, (150, 250)) 

		# convert f clef to numpy arrays and make them with correct size 
		imgBass = cv2.imread('./assets/fclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgBassBW) = cv2.threshold(imgBass, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgBassResized = cv2.resize(imgBassBW, (150, 250))

		staffLineCount = 0 

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# put gclef
			if staffLineCount % 2 == 0:
				# for the rows in the clef
				for i in range(250):
					#for columns in the clef
					for j in range(150):
						# check if there is black pixel there
						if imgTrebleResized[i][j] == 0:
							notesArr[i + staffLineStartingPos][j + column] = 0
			else:
				# for the rows in the clef
				for i in range(250):
					#for columns in the clef
					for j in range(150):
						# check if there is black pixel there
						if imgBassResized[i][j] == 0:
							notesArr[i + staffLineStartingPos][j + column] = 0

			staffLineCount += 1


		notesArr = notesArr * 255
		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 0:
		# just treble clef

		# convert g clef to numpy arrays and make them with correct size 
		imgTreble = cv2.imread('./assets/gclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgTrebleBW) = cv2.threshold(imgTreble, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgTrebleResized = cv2.resize(imgTrebleBW, (150, 250)) 

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(250):
				#for columns in the clef
				for j in range(150):
					# check if there is black pixel there
					if imgTrebleResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		notesArr = notesArr * 255
		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 2:
		# just bass clef

		# convert f clef to numpy arrays and make them with correct size 
		imgBass = cv2.imread('./assets/fclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgBassBW) = cv2.threshold(imgBass, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgBassResized = cv2.resize(imgBassBW, (150, 250))

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(250):
				#for columns in the clef
				for j in range(150):
					# check if there is black pixel there
					if imgBassResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		notesArr = notesArr * 255
		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 3:
		# just alto clef

		# convert c clef to numpy arrays and make them with correct size 
		imgBass = cv2.imread('./assets/cclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgAltoBW) = cv2.threshold(imgAlto, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgAltoResized = cv2.resize(imgAltoBW, (150, 250))

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(250):
				#for columns in the clef
				for j in range(150):
					# check if there is black pixel there
					if imgAltoResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		notesArr = notesArr * 255
		cv2.imwrite("clefs.jpg", notesArr)


	# return the modified notes array with the clefs
	return notesArr



def placeNotes(notesData, notesArr, staffLinesStartingPos):

	# must start at position 350 now in terms of the columns

	durationCount = 0

	for note in notes:

		# need to move to next staff line
		if durationCount % 4 == 0:
			continue

		# can stay on same staff line but shift the notes over a bit
		else:
			noteType = getNoteType(note['note'], note['pitch'], note['length'])




# returns the name of the converted pdf
def conversion(file, fileName):
	# fileName = 'hello.mid'

	# substitute this with the place where MuseScore is stored
	# cmd = "/Applications/MuseScore\ 3.app/Contents/MacOS/mscore -o "

	# creating the name for the pdf
	# pdfName = "'" + fileName[:fileName.find('.')] + '.pdf' "' "
	# cmd = cmd + pdfName + "'" + fileName + "'"

	# making the system call with the command for conversion
	# os.system(cmd)

	return pdfName



notes = getNotes('./MusicSheet1.json')
notesArrWithLines, staffLinesStartingPos = createLines(notes)
notesArrWithClefs = placeClefs(notes, notesArrWithLines, staffLinesStartingPos)
notesArrWithNotes = placeNotes(notes, notesArrWithLines, staffLinesStartingPos)

