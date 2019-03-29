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

	print note
	print pitch
	print length
	noteType = False

	if note == 0 and pitch == 1 and length == 0:
		noteType = 'gclef'
	elif note == 6 and pitch == 1 and length == 0:
		noteType = 'fclef'
	elif note == 7 and pitch == 1 and length == 0:
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
	currColumn = 350

	durationCount = 0

	# indicate which row to look at 
	k = 0

	print notesData

	# for each of the notes in the notesData
	for note in notesData['notes']:

		# get the note nype and get the corresponding file
		noteType = getNoteType(note['note'], note['pitch'], note['length'])
		noteFile = './assets/' + noteType + '.png'
		imgNote = cv2.imread(noteFile, cv2.IMREAD_GRAYSCALE)
		(thresh, imgNoteBW) = cv2.threshold(imgNote, 128, 255, cv2.THRESH_BINARY)
		imgNoteResized = cv2.resize(imgNoteBW, (150, 250))

		name = noteType + '.png'

		imgNoteResized = imgNoteResized * 255
		cv2.imwrite(name, imgNoteResized)

		# check the note type and do spacing and fill in note
		if noteType == 'sixteenth':
			# through the row
			for i in range(250):

				# through the column
				for j in range(150):

					if imgNoteResized[i][j] == 0:
						# check if there is note there
						print staffLinesStartingPos[k] + (note['pitch'] * 10)
						print currColumn + j
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 10

		elif noteType == 'eighth':
			# through the row
			for i in range(250):

				# through the column
				for j in range(150):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 20

		elif noteType == 'quarter':
			# through the row
			for i in range(250):

				# through the column
				for j in range(150):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 40

		elif noteType == 'half':
			print 'HERE!!!!\n\n'
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						print staffLinesStartingPos[k]
						print staffLinesStartingPos[k] + (note['pitch'] * 10)
						print currColumn + j
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 20)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 80

		elif noteType == 'whole':
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 160

		elif noteType == 'sharp':
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 5
		
		elif noteType == 'flat':
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 5

		elif noteType == 'eighthrest' or noteType == 'quarterrest' or noteType == 'wholerest':
			# through the row
			for i in range(imgNoteResized.shape[0]):

				# through the column
				for j in range(imgNoteResized.shape[1]):

					if imgNoteResized[i][j] == 0:
					# check if there is note there
						notesArr[staffLinesStartingPos[k] + (note['pitch'] * 10)][currColumn + j] = 0

			# move the column position for spacing after the note
			currColumn = currColumn + imgNoteResized.shape[1] + 5

		# add to the duration of the notes
		durationCount += note['length']

		# need to move to next staff line if the current staff line is full
		# rest the current column position to be beginning of the line
		if durationCount == int(durationCount) and durationCount % 16 == 0:
			print "MOVIGN TO NEXT LINE"
			k += 1
			currColumn = 350


	notesArr = notesArr * 255
	cv2.imwrite("notes.png", notesArr)



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



# notes = getNotes('./MusicSheet1.json')
notesArrWithLines, staffLinesStartingPos = createLines(notes)
notesArrWithClefs = placeClefs(notes, notesArrWithLines, staffLinesStartingPos)
notesArrWithNotes = placeNotes(notes, notesArrWithClefs, staffLinesStartingPos)

