from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect


# https://pythonhosted.org/Flask-Mail/
def selectMusic():
    content = request.json

    print content['instrument']
    
    MySQLConnect.updateInstrumentById("sheet_music", content['sheet_id'], content['instrument'])

    return 'Music Selected!'