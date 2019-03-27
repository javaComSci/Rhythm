from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect
from flask_mail import Mail, Message
import convertToPDF
import random


# https://pythonhosted.org/Flask-Mail/
def exportPDF(mail):
    content = request.json

    information = MySQLConnect.findSheetBySheetID("sheet_music", content['sheet_id'])
    
    file = information['file']
    name = information['name']

    pdfName = convertToPDF.conversion(file, name)

    messageTitle = fileName + ' Converted to PDF'
    msg = Message(messageTitle, sender = content['email'], recipients = [content['email']])

    msg.body = "Here is your requested music in pdf version."

    with app.open_resource(pdfName) as fp:
        msg.attach(pdfName, "application/pdf", fp.read())

    mail.send(msg)


    return 'sent'