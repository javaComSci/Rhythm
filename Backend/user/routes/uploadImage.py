from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64
import random
import sys
# from conversion import conv

# from NotesRecognization.conversion import conv

imgs = []
widths = []
heights = []
Xs = []
Ys = []

def cameraPipeline():
	
	content = request.json

	if 'img_data' not in content.keys():
		return 'No image given'

	if 'sheet_id' not in content.keys():
		return 'Not valid sheet id'

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
		imgs.append(img_data)
		widths.append(boxWidth)
		heights.append(boxHeight)
		Xs.append(X)
		Ys.append(Y)

	#for img_file in img_data:
	img = base64.b64decode(img_data)
		# randInt = random.randint(1, 20000)
		# randStr = str(randInt)
		# filename = randStr + '.jpg'

	with open(filename, 'wb') as f:
	    f.write(img)

	# check if all images have been recieved
	if flag == True:
		jsonName = conv(imgs, Xs, Ys, widths, heights)
		imgs = []
		filee = open("/home/Rhythm/Backend/"+jsonName)
		fileee = json.load(filee)
		filee.close()
		return fileee

	return 'In Progress'
       # return "{}"
