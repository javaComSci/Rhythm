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
		noteType = 'gclef'
	elif note == 7 and pitch == 1 and length == 0:
		noteType = 'fclef'
	elif note == 6 and pitch == 1 and length == 0:
		noteType = 'cclef'
	elif note == 5:
		noteType = 'sixteenth'
	elif note == 1:
		noteType = 'eighth'
	elif note == 2:
		noteType = 'quarter'
	elif note == 3:
		noteType = 'half'
	elif note == 4:
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

	# find number of measures needed
	measures = int(math.ceil(duration/4))

	# find number of staff lines needed
	staffLines = int(math.ceil(duration/16))

	# total size needed for numpy array, which is A4 size
	notesArr = np.ones((8300, 4550))

	print("MEASURES", measures, staffLines)

	# initial starting point for putting the pixels
	row = 400

	staffLinesStartingPos = []

	# add the lines for the staff lines
	for staffLine in range(staffLines):

		staffLinesStartingPos.append(row)

		# need 5 lines for each row
		for i in range(5):

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




def createVerticalLines(notesData, notesArr, staffLinesStartingPos):

	colPos = 1350

	measureLinesStartingPos = []

	# for each of the staff lines
	for staffLine in staffLinesStartingPos:

		# the number of measures
		for k in range(4):

			if len(measureLinesStartingPos) < 4:
				measureLinesStartingPos.append(colPos)

			# to add the vertical line for the height
			for i in range(200):

				# for the thickness of the line
				for j in range(10):

					notesArr[staffLine + i][colPos + j] = 0

			colPos += 1000

		colPos = 1350

	return notesArr, measureLinesStartingPos


def placeClefs(notesData, notesArr, staffLinesStartingPos):
	if notesData['clef'] == 1:
		# both clefs, need to alternate

		# convert g clef to numpy arrays and make them with correct size
		imgTreble = cv2.imread('./assets/gclef.jpg', cv2.IMREAD_GRAYSCALE)
		(thresh, imgTrebleBW) = cv2.threshold(imgTreble, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgTrebleResized = cv2.resize(imgTrebleBW, (200, 250))

		# convert f clef to numpy arrays and make them with correct size
		imgBass = cv2.imread('./assets/fclef.jpg', cv2.IMREAD_GRAYSCALE)
		(thresh, imgBassBW) = cv2.threshold(imgBass, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgBassResized = cv2.resize(imgBassBW, (200, 250))

		staffLineCount = 0

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# put gclef
			if staffLineCount % 2 == 0:
				# for the rows in the clef
				for i in range(imgTrebleResized.shape[0]):
					#for columns in the clef
					for j in range(imgTrebleResized.shape[1]):
						# check if there is black pixel there
						if imgTrebleResized[i][j] == 0:
							notesArr[i + staffLineStartingPos][j + column] = 0
			else:
				# for the rows in the clef
				for i in range(imgBassResized.shape[0]):
					#for columns in the clef
					for j in range(imgBassResized.shape[1]):
						# check if there is black pixel there
						if imgBassResized[i][j] == 0:
							notesArr[i + staffLineStartingPos][j + column] = 0

			staffLineCount += 1

		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 0:
		# just treble clef

		# convert g clef to numpy arrays and make them with correct size
		imgTreble = cv2.imread('./assets/gclef.jpg', cv2.IMREAD_GRAYSCALE)
		(thresh, imgTrebleBW) = cv2.threshold(imgTreble, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgTrebleResized = cv2.resize(imgTrebleBW, (200, 250))

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(imgTrebleResized.shape[0]):
				#for columns in the clef
				for j in range(imgTrebleResized.shape[1]):
					# check if there is black pixel there
					if imgTrebleResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 2:
		# just bass clef

		# convert f clef to numpy arrays and make them with correct size
		imgBass = cv2.imread('./assets/fclef.jpg', cv2.IMREAD_GRAYSCALE)
		(thresh, imgBassBW) = cv2.threshold(imgBass, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgBassResized = cv2.resize(imgBassBW, (200, 250))

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(imgBassResized.shape[0]):
				#for columns in the clef
				for j in range(imgBassResized.shape[1]):
					# check if there is black pixel there
					if imgBassResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		cv2.imwrite("clefs.jpg", notesArr)


	elif notesData['clef'] == 3:
		# just alto clef

		# convert c clef to numpy arrays and make them with correct size
		imgBass = cv2.imread('./assets/cclef.png', cv2.IMREAD_GRAYSCALE)
		(thresh, imgAltoBW) = cv2.threshold(imgAlto, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		imgAltoResized = cv2.resize(imgAltoBW, (200, 250))

		for staffLineStartingPos in staffLinesStartingPos:

			# current column position on the staff line
			column = 200

			# for the rows in the clef
			for i in range(imgAltoResized.shape[0]):
				#for columns in the clef
				for j in range(imgAltoResized.shape[1]):
					# check if there is black pixel there
					if imgAltoResized[i][j] == 0:
						notesArr[i + staffLineStartingPos][j + column] = 0

		cv2.imwrite("clefs.jpg", notesArr)


	# return the modified notes array with the clefs
	return notesArr



def placeTime(notesData, notesArr, staffLinesStartingPoss):
	imgTime = cv2.imread('./assets/44time.jpg', cv2.IMREAD_GRAYSCALE)
	(thresh, imgTimeBW) = cv2.threshold(imgTime, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	imgTimeResized = cv2.resize(imgTimeBW, (150, 250))

	currCol = colLeft + 200

	for staffLineStartingPos in staffLinesStartingPos:

		# for each of the rows
		for i in range(imgTimeResized.shape[0]):

			# for each of the columns
			for j in range(imgTimeResized.shape[1]):

				if imgTimeResized[i][j] == 0:
					notesArr[staffLineStartingPos + i - 20][currCol + j] = 0

	cv2.imwrite("time.jpg", notesArr)

	return notesArr



def placeNotes(notesData, notesArr, staffLinesStartingPos, measureLinesStartingPos):

	# must start at position now in terms of the columns
	currColumn = 600

	durationCount = 0

	# indicate which row to look at for the starting positions
	k = 0

	# for each of the notes in the notesData
	for note in notesData['notes']:

		# get the note type and get the corresponding file
		noteType = getNoteType(note['note'], note['pitch'], note['length'])
		noteFile = './assets/' + noteType + '.jpg'
		imgNote = cv2.imread(noteFile, cv2.IMREAD_GRAYSCALE)
		(thresh, imgNoteBW) = cv2.threshold(imgNote, 128, 255, cv2.THRESH_BINARY)
		imgNoteResized = cv2.resize(imgNoteBW, (150, 250))

		name = noteType + '.jpg'

		# check the note type and do spacing and fill in note
		if noteType == 'sixteenth':

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + (note['pitch'] * 25)

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + 50

		elif noteType == 'eighth':

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + (note['pitch'] * 25)

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + 100

		elif noteType == 'quarter':

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + (note['pitch'] * 25)

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 100

		elif noteType == 'half':

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + (note['pitch'] * 25)

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 320


		elif noteType == 'whole':

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + (note['pitch'] * 25)

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 500


		elif noteType == 'sharp':
			imgNoteResized = cv2.resize(imgNoteResized, (70, 70))

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + 10

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			# currColumn = currColumn + 10

		elif noteType == 'flat':

			imgNoteResized = cv2.resize(imgNoteResized, (70, 70))

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there

						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + 10

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			# currColumn = currColumn + 10

		elif noteType == 'eighthrest' or noteType == 'quarterrest':
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + 200

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			if noteType == 'eighthrest':
				# move the column position for spacing after the note
				currColumn = currColumn + imgNoteResized.shape[1] - 25
			elif noteType == 'quarterrest':
				# move the column position for spacing after the note
				currColumn = currColumn + imgNoteResized.shape[1] + 100

		elif noteType == 'halfrest':
			imgNoteResized = cv2.resize(imgNoteResized, (90, 70))

			# need to move it for some space
			currColumn = currColumn + 10
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + 130

						# keep track of the column needed
						pixelCol = currColumn + j

						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 290

		elif noteType == 'wholerest':

			imgNoteResized = cv2.resize(imgNoteResized, (230, 230))
			print("THE SHAPE OF THE OBJECT IS ", imgNoteResized.shape)

			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
						# need to shift everything up first so that the bottom of the note is first touching the top of the line
						pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0]

						# need to shift the note down for the pitch
						pixelRow = pixelRow + 141

						# keep track of the column needed
						pixelCol = currColumn + j

						print("PIXEL ROW", pixelRow, pixelCol)


						notesArr[pixelRow + i][pixelCol] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 300


		# add to the duration of the notes
		durationCount += note['length']

		print("THE CURRENT COLUMN", currColumn)

		print("MEASURE LINES POS", measureLinesStartingPos)
		# align for the first measure
		if durationCount == int(durationCount) and durationCount % 4 == 0 and durationCount % 16 != 0 and durationCount != 0:
			currColumn = measureLinesStartingPos[int((durationCount % 16)/4) - 1]


		# need to move to next staff line if the current staff line is full
		# rest the current column position to be beginning of the line
		if durationCount == int(durationCount) and durationCount % 16 == 0 and durationCount != 0:
			print "MOVIGN TO NEXT LINE"
			k += 1
			currColumn = 600

	print("THIS IS IN THE NOTES ARRAY PRINTING\n\n\n\n")
	cv2.imwrite("notes.jpg", notesArr)



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
notesArrWithVerticalLines, measureLinesStartingPos = createVerticalLines(notes, notesArrWithLines, staffLinesStartingPos)
notesArrWithClefs = placeClefs(notes, notesArrWithVerticalLines, staffLinesStartingPos)
notesArrWithTime = placeTime(notes, notesArrWithClefs, staffLinesStartingPos)
notesArrWithNotes = placeNotes(notes, notesArrWithTime, staffLinesStartingPos, measureLinesStartingPos)
