from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect
from flask_mail import Mail, Message
import convertToPDF
import random


# https://pythonhosted.org/Flask-Mail/
def exportPDF(mail, app):
    content = request.json
    print('{} and {}'.format(content['sheet_ids'], content['email']))

    messageTitle = 'PDF Conversion from Rhythm'
    msg = Message(messageTitle, sender = content['email'], recipients = [content['email']])
    msg.body = "Here is your requested music in pdf version."

    for sheet_id in content['sheet_ids']:
        # information = MySQLConnect.findSheetBySheetID("sheet_music", 222)
        information = MySQLConnect.findSheetBySheetID("sheet_music", sheet_id)
        print "INFORMATION"
        print information
    
        # has the actual information in the file
        file = information[0][1]

        # has the file name
        name = information[0][3]

        # need to change this to be the name of the converted file
        # pdfName = convertToPDF.conversion(file, name)
        pdfName = 'user/routes/hello.pdf'

        with app.open_resource(pdfName) as fp:
            msg.attach(pdfName, "application/pdf", fp.read())

    mail.send(msg)

    return 'sent'