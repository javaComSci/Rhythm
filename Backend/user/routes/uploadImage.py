from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect
import base64

def cameraPipeline():
	content = request.json
	img_data = content['img_data']

	img = base64.b64decode(img_data)
	filename = 'food1.jpg'
	with open(filename, 'wb') as f:
		f.write(img)

	# print("IMG DATA", imgdata)
	# fh = open("uploadedImage.png", "wb")
	# fh.write(img_data.decode('base64'))
	# fh.close()

	return img_data
