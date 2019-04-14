from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64
import random
import sys
# from conversion import conv

# from NotesRecognization.conversion import conv

imgs = []

def cameraPipeline():
	
	content = request.json

	# img data as an array with all the filepaths
	img_data = content['img_data']
	flag = content['final'] 
	sheetID = content['sheetID']
	compID = content['compID']

	filename = './convertedData/{}-{}.jpg'.format(sheetID, compID)
	global imgs
	imgs.append(filename)

	img = base64.b64decode(img_file)
	# randInt = random.randint(1, 20000)
	# randStr = str(randInt)
	# filename = randStr + '.jpg'

	with open(filename, 'wb') as f:
	    f.write(img)

	# check if all images have been recieved
	if flag == True:
	    # jsonName = conv(imgs)
	    imgs = []

	return 'cameraPipeline'