from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

def cameraPipeline():
    content = request.json
    data = content['formData']
    print("THE FORM DATA", data)
    fh = open("uploadedImage.png", "wb")
    fh.write(data.decode('base64'))
    # fh.close()
    return 'uploaded'
