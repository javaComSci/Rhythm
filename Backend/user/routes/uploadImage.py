from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64

imgs = []

def cameraPipeline():
	content = request.json
	img_data = content['img_data']
        flag = content['final'] 
        sheetID = content['sheetID']
        compID = content['compID']
	img = base64.b64decode(img_data)
	filename = '{}-{}.jpg'.format(sheetID, compID)
	with open(filename, 'wb') as f:
		f.write(img)
        imgs.append(filename)
        if(flag){
            # Send to richard

        }
	# print("IMG DATA", imgdata)
	# fh = open("uploadedImage.png", "wb")
	# fh.write(img_data.decode('base64'))
	# fh.close()

	return img_data
