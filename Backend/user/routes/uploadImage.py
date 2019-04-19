from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64
import random
import sys
from conversion import conv

# from NotesRecognization.conversion import conv

imgs = []
widths = []
heights = []
Xs = []
Ys = []

def cameraPipeline():
	print("IN CAMERA PIPELELINE!!!!!")

	content = request.json

	if 'img_data' not in content.keys():
		return 'No image given'

	print("AFTER IMAGE GIVEN")

	if 'sheetID' not in content.keys():
		return 'Not valid sheet id'

	print("PIPELINE")

	# img data as an array with all the filepaths
	img_data = content['img_data']
	flag = content['final']
	sheetID = content['sheetID']
	compID = content['compID']
	boxHeight = content['boxHeight']
	boxWidth = content['boxWidth']
	X = content['X']
	Y = content['Y']

	filename = '/home/Rhythm/Backend/user/routes/convertedData/{}-{}.jpg'.format(sheetID, compID)
	global imgs, widths, heights, Xs, Ys
	if img_data is not None:
		print("THE DATA IS NOT NONE")
		imgs.append(filename)
		widths.append(boxWidth)
		heights.append(boxHeight)
		Xs.append(X)
		Ys.append(Y)
	print("AFTER THE DATA")

	#for img_file in img_data:
	img = base64.b64decode(img_data)
		# randInt = random.randint(1, 20000)
		# randStr = str(randInt)
		# filename = randStr + '.jpg'

	with open(filename, 'wb') as f:
	    f.write(img)

	# check if all images have been recieved
	if flag == True:
		print("PUT IN THE CONVERSION AND FLAG IS TRUE")
		jsonName = conv(imgs, Xs, Ys, widths, heights)
		imgs = []
		filee = open("/home/Rhythm/Backend/"+jsonName)
		fileee = json.load(filee)
		filee.close()
		return fileee

	return 'In Progress'
       # return "{}"
