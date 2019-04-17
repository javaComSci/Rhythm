from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect
from flask_mail import Mail, Message
import random
import os
import json
import math
import cv2
import numpy as np
import img2pdf
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

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
    print("I GOT", note, pitch, length)
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
    elif note == 8:
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


def createTitle(sheetid):
    # total size needed for numpy array, which is A4 size
    # 5900 is the ideal space for a single page
    notesArr = np.ones((5350 * 2, 4550)) * 255

    for i in range(1125, 3375):
        for j in range(4):
            notesArr[400 + j][i] = 0

    for i in range(1800, 2700):
        for j in range(4):
            notesArr[550 + j][i] = 0

    return notesArr


def createLines(notesArr, notes):

    duration = 0

    # find total duration of notes
    for note in notes['notes']:
        if note['note'] <= 14:
            duration += note['length']

    # find number of measures needed
    measures = int(math.ceil(duration/4))

    # find number of staff lines needed
    staffLines = int(math.ceil(duration/16))

    # print("MEASURES", duration, measures, staffLines)

    # initial starting point for putting the pixels
    row = 1000

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


    # notesArr = notesArr * 255
    # cv2.imwrite("lines.jpg", notesArr)

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
            column = 150

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
            column = 150

            # for the rows in the clef
            for i in range(imgTrebleResized.shape[0]):
                #for columns in the clef
                for j in range(imgTrebleResized.shape[1]):
                    # check if there is black pixel there
                    if imgTrebleResized[i][j] == 0:
                        notesArr[i + staffLineStartingPos][j + column] = 0

       #  cv2.imwrite("clefs.jpg", notesArr)


    elif notesData['clef'] == 2:
        # just bass clef

        # convert f clef to numpy arrays and make them with correct size
        imgBass = cv2.imread('./assets/fclef.jpg', cv2.IMREAD_GRAYSCALE)
        (thresh, imgBassBW) = cv2.threshold(imgBass, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        imgBassResized = cv2.resize(imgBassBW, (200, 250))

        for staffLineStartingPos in staffLinesStartingPos:

            # current column position on the staff line
            column = 150

            # for the rows in the clef
            for i in range(imgBassResized.shape[0]):
                #for columns in the clef
                for j in range(imgBassResized.shape[1]):
                    # check if there is black pixel there
                    if imgBassResized[i][j] == 0:
                        notesArr[i + staffLineStartingPos][j + column] = 0

        # cv2.imwrite("clefs.jpg", notesArr)


    elif notesData['clef'] == 3:
        # just alto clef
        print("DOING THE CCLEF")
        # convert c clef to numpy arrays and make them with correct size
        imgAlto = cv2.imread('./assets/cclef.jpg', cv2.IMREAD_GRAYSCALE)
        (thresh, imgAltoBW) = cv2.threshold(imgAlto, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        imgAltoResized = cv2.resize(imgAltoBW, (200, 250))

        for staffLineStartingPos in staffLinesStartingPos:

            # current column position on the staff line
            column = 150

            # for the rows in the clef
            for i in range(imgAltoResized.shape[0]):
                #for columns in the clef
                for j in range(imgAltoResized.shape[1]):
                    # check if there is black pixel there
                    if imgAltoResized[i][j] == 0:
                        notesArr[i + staffLineStartingPos][j + column] = 0

        # cv2.imwrite("clefs.jpg", notesArr)


    # return the modified notes array with the clefs
    return notesArr



def placeTime(notesData, notesArr, staffLinesStartingPos):
    imgTime = cv2.imread('./assets/44time.jpg', cv2.IMREAD_GRAYSCALE)
    (thresh, imgTimeBW) = cv2.threshold(imgTime, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    imgTimeResized = cv2.resize(imgTimeBW, (150, 250))

    currCol = colLeft + 150

    for staffLineStartingPos in staffLinesStartingPos:

        # for each of the rows
        for i in range(imgTimeResized.shape[0]):

            # for each of the columns
            for j in range(imgTimeResized.shape[1]):

                if imgTimeResized[i][j] == 0:
                    notesArr[staffLineStartingPos + i - 20][currCol + j] = 0

    # cv2.imwrite("time.jpg", notesArr)

    return notesArr



def placeNotes(notesData, notesArr, staffLinesStartingPos, measureLinesStartingPos):

    # must start at position now in terms of the columns
    currColumn = 450

    durationCount = 0

    # indicate which row to look at for the starting positions
    k = 0

    # for each of the notes in the notesData
    for note in notesData['notes']:

        # get the note type and get the corresponding file
        noteType = getNoteType(note['note'], note['pitch'], note['length'])

        if noteType == 'gclef' or noteType == 'cclef' or noteType == 'fclef' or noteType == False:
            continue

        noteFile = './assets/' + noteType + '.jpg'
        imgNote = cv2.imread(noteFile, cv2.IMREAD_GRAYSCALE)
        (thresh, imgNoteBW) = cv2.threshold(imgNote, 128, 255, cv2.THRESH_BINARY)
        imgNoteResized = cv2.resize(imgNoteBW, (150, 250))

        name = noteType + '.jpg'

        if currColumn + imgNoteResized.shape[1] > colRight + 30:
            print("IGNORING NOTE")
            continue

        # check the note type and do spacing and fill in note
        if noteType == 'sixteenth':
            print("sixteenth")

            if note['pitch'] == 10 or  note['pitch'] == 11 or note['pitch'] == 12:
                for i in range(staffLinesStartingPos[k] + 245, staffLinesStartingPos[k] + 250):
                    for j in range(currColumn + 25, currColumn + 90):
                        notesArr[i][j] = 0

            # through the row
            for i in range(imgNoteResized.shape[0]):

                # through the column
                for j in range(imgNoteResized.shape[1]):

                    if imgNoteResized[i][j] == 0:
                    # check if there is note there

                        # need to shift everything up first so that the bottom of the note is first touching the top of the line
                        pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0] + 20

                        # need to shift the note down for the pitch
                        pixelRow = pixelRow + (note['pitch'] * 25)

                        # keep track of the column needed
                        pixelCol = currColumn + j

                        notesArr[pixelRow + i][pixelCol] = 0

            # move the column position for spacing after the note
            currColumn = currColumn + 45

             # add to the duration of the notes
            durationCount += note['length']

        elif noteType == 'eighth':
            print("eighth")
            # below the given lines so need to add in a new line
            if note['pitch'] == 10 or  note['pitch'] == 11 or note['pitch'] == 12:
                for i in range(staffLinesStartingPos[k] + 245, staffLinesStartingPos[k] + 250):
                    for j in range(currColumn + 25, currColumn + 90):
                        notesArr[i][j] = 0
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

             # add to the duration of the notes
            durationCount += note['length']

        elif noteType == 'quarter':
            # below the given lines so need to add in a new line
            if note['pitch'] == 10 or note['pitch'] == 11 or note['pitch'] == 12:
                for i in range(staffLinesStartingPos[k] + 245, staffLinesStartingPos[k] + 250):
                    for j in range(currColumn + 10, currColumn + 130):
                        notesArr[i][j] = 0

            print("quarter")
            # through the row
            for i in range(imgNoteResized.shape[0]):

                # through the column
                for j in range(imgNoteResized.shape[1]):

                    if imgNoteResized[i][j] == 0:
                    # check if there is note there

                        # need to shift everything up first so that the bottom of the note is first touching the top of the line
                        pixelRow = staffLinesStartingPos[k-1] - imgNoteResized.shape[0] 

                        # need to shift the note down for the pitch
                        pixelRow = pixelRow + (note['pitch'] * 25)

                        # keep track of the column needed
                        pixelCol = currColumn + j

                        notesArr[pixelRow + i][pixelCol] = 0

            # move the column position for spacing after the note
            currColumn = currColumn + imgNoteResized.shape[1] + 100

             # add to the duration of the notes
            durationCount += note['length']

        elif noteType == 'half':
            print("half")

            # below the given lines so need to add in a new line
            if note['pitch'] == 10 or note['pitch'] == 11 or note['pitch'] == 12:
                for i in range(staffLinesStartingPos[k] + 245, staffLinesStartingPos[k] + 250):
                    for j in range(currColumn + 10, currColumn + 130):
                        notesArr[i][j] = 0

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
            currColumn = currColumn + imgNoteResized.shape[1] + 300

             # add to the duration of the notes
            durationCount += note['length']


        elif noteType == 'whole':   
            imgNoteResized = cv2.resize(imgNoteResized, (250, 200))

            print("whole")
            if note['pitch'] == 10 or note['pitch'] == 11 or note['pitch'] == 12:
                for i in range(staffLinesStartingPos[k] + 245, staffLinesStartingPos[k] + 250):
                    for j in range(currColumn + 70, currColumn + 160):
                        notesArr[i][j] = 0
            # through the row
            for i in range(imgNoteResized.shape[0]):

                # through the column
                for j in range(imgNoteResized.shape[1]):

                    if imgNoteResized[i][j] == 0:
                    # check if there is note there

                        # need to shift everything up first so that the bottom of the note is first touching the top of the line
                        pixelRow = staffLinesStartingPos[k] - imgNoteResized.shape[0] + 55

                        # need to shift the note down for the pitch
                        pixelRow = pixelRow + (note['pitch'] * 25)

                        # keep track of the column needed
                        pixelCol = currColumn + j

                        notesArr[pixelRow + i][pixelCol] = 0

            # move the column position for spacing after the note
            currColumn = currColumn + imgNoteResized.shape[1] + 500

             # add to the duration of the notes
            durationCount += note['length']


        elif noteType == 'sharp':
            print("sharp")
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
            print("flat")
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
            print("rest-eighth")
            if noteType == 'eighthrest':
                imgNoteResized = cv2.resize(imgNoteResized, (100, 150))

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

             # add to the duration of the notes
            durationCount += note['length']

        elif noteType == 'halfrest':
            print("halfrest")
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

             # add to the duration of the notes
            durationCount += note['length']

        elif noteType == 'wholerest':
            print("wholerest")
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

                        notesArr[pixelRow + i][pixelCol] = 0

            # move the column position for spacing after the note
            currColumn = currColumn + imgNoteResized.shape[1] + 300

            # add to the duration of the notes
            durationCount += note['length']

        # align for the first measure
        if durationCount == int(durationCount) and durationCount % 4 == 0 and durationCount % 16 != 0 and durationCount != 0:
            currColumn = measureLinesStartingPos[int((durationCount % 16)/4) - 1]
        # need to move to next staff line if the current staff line is full
        # rest the current column position to be beginning of the line
        elif durationCount == int(durationCount) and durationCount % 16 == 0 and durationCount != 0:
            print("GOING TO THE NEXT LINE", durationCount, k)
            currColumn = 450
            if noteType != 'sharp' and noteType != 'flat' and noteType != 'cclef' and noteType != 'gclef' and noteType != 'fclef':
                k += 1
            

    print("THIS IS IN THE NOTES ARRAY PRINTING\n\n\n\n")
    cv2.imwrite("./notes.jpg", notesArr)
    print("AFTER THE WRITE")

    return notesArr


# returns the name of the converted pdf
# takes in the id of the sheet that needs to be converted
def pdfPipeline(sheetId, fileInfo):

    # get the name of the sheet with the json extension
    sheetIdWithJSONExtension = str(sheetId) + ".json"

    # testing with the actual json
    # notes = getNotes(sheetIdWithJSONExtension)

    notes = fileInfo
    print("THE STUFF IN THE FILE ARE", notes)

    notesWithTitleLine = createTitle(sheetId)
    notesArrWithLines, staffLinesStartingPos = createLines(notesWithTitleLine, notes)
    notesArrWithVerticalLines, measureLinesStartingPos = createVerticalLines(notes, notesArrWithLines, staffLinesStartingPos)
    notesArrWithClefs = placeClefs(notes, notesArrWithVerticalLines, staffLinesStartingPos)
    notesArrWithTime = placeTime(notes, notesArrWithClefs, staffLinesStartingPos)
    notesArrWithNotes = placeNotes(notes, notesArrWithTime, staffLinesStartingPos, measureLinesStartingPos)

    pdfNames = []

    #break up the image into many images
    for i in range(2):
        # save the image in a jpg
        jpgName = "./convertedData/" + str(sheetId) + "number" + str(i) + ".jpg"

        # break it up into multiple pieces
        miniNotes = notesArrWithNotes[i * 5350:(i+1) * 5350,]

        # checking if there are any black pixels
        exist = False

        # check if there are any notes in this or not
        # check if not all of them are not white
        if np.all(miniNotes == 255) == False:
            exist = True
        # for j in range(miniNotes.shape[0]):
        #     for k in range(miniNotes.shape[1]):
        #         if miniNotes[j][k] == 0:
        #             exist = True

        # means that there are no black pixels and it is okay to do that
        if exist == False:
            break

        cv2.imwrite(jpgName, miniNotes)

        # get the name of the file in pdf form
        pdfName = "./convertedData/" + str(sheetId) + ":Page-" + str(i + 1) + ".pdf"
        pdfFile = open(pdfName, "wb")

        # save it as the pdf
        pdfBytes = img2pdf.convert(jpgName)

        pdfFile.write(pdfBytes)

        # just the name of the pdf
        pdfNames.append(str(sheetId) + ":Page-" + str(i + 1) + '.pdf')
    
    return pdfNames


# https://pythonhosted.org/Flask-Mail/
def exportPDF(mail, app):
    content = request.json
    print('{} and {}'.format(content['sheet_ids'], content['email']))

    messageTitle = 'PDF Conversion from Rhythm'
    msg = Message(messageTitle, sender = content['email'], recipients = [content['email']])
    msg.body = "Here is your requested music in pdf version."

    flag = False

    for sheet_id in content['sheet_ids']:
        information = MySQLConnect.findSheetBySheetID("sheet_music", int(sheet_id))

        if information == None or len(information) == 0:
            flag = True
            continue

        print(information)
    
        # has the actual information in the file
        file1 = json.loads(information[0][4].decode('string-escape').strip('"'))
        # file1 = information['notes']

        # has the file name
        name = information[0][3]

        # need to change this to be the name of the converted file
        # pdfNames = pdfPipeline(sheet_id, file)

        # json for testing purpose
        # file = open('./MusicSheet1.json')
        # notes = json.load(file)
        # file.close()

        # call to create the pdf for that image
        pdfNames = pdfPipeline(sheet_id, file1)

        print("THE NAME OF THE PDF", pdfNames)
        # if multiple pdfs are created, then send each one of them and they exist
        if len(pdfNames) > 0:
            for pdfName in pdfNames:
                with app.open_resource('convertedData/' + pdfName) as fp:
                    msg.attach(name + '-' + pdfName, "application/pdf", fp.read())
                # app.close_resource('convertedData/' + pdfName)
    mail.send(msg)

    if flag == True:
        return 'Some Sheets Missing'

    return 'Sent All Successfully'


def testing():
    file = open('./MusicSheet5.json')
    notes = json.load(file)
    file.close()
    pdfNames = pdfPipeline(222, notes)

# testing()
