from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64
import random
import sys

# from NotesRecognization.conversion import conv

imgs = []

def cameraPipeline():
	
	content = request.json

	# img data as an array with all the filepaths
	img_data = content['img_data']
        flag = content['final'] 
        sheetID = content['sheetID']
        compID = content['compID']
	img = base64.b64decode(img_data)

	filename = '{}-{}.jpg'.format(sheetID, compID)
        imgs.append(filename)
            # Send to richard


	# filePathsToConvert = []

	#for img_file in img_data:

	img = base64.b64decode(img_file)
		# randInt = random.randint(1, 20000)
		# randStr = str(randInt)
		# filename = randStr + '.jpg'

	with open(filename, 'wb') as f:
	    f.write(img)
    
	# filePathsToConvert.append(filename)

	# print("IMG DATA", imgdata)
	# fh = open("uploadedImage.png", "wb")
	# fh.write(img_data.decode('base64'))
	# fh.close()
        if flag == True:
            jsonName = conversion.conv(imgs)
            imgs = []

	return 'cameraPipeline'
