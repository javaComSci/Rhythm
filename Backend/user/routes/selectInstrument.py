from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect


# https://pythonhosted.org/Flask-Mail/
def selectMusic():
    info = request.json

    # print content['instrument']
    # if no instrument was provided, default to piano
    instrument = info['instrument']

    if type(instrument) == int:
    	MySQLConnect.updateInstrumentById('sheet_music', info['sheet_id'], 'Piano')
    	return 'false'

    validInstruments = ['Piano', 'Harp', 'Violin', 'Flute', 'Tuba', 'Guitar', 'Cello', 'Bass', 'Trombone', 'Viola']
    if instrument not in validInstruments:
    	print("HERE")
    	info['instrument'] = 'Piano'
    	instrument = info['instrument']
    
    
    MySQLConnect.updateInstrumentById('sheet_music', info['sheet_id'], info['instrument'])

    print("IN SELECT MUSIC", info['instrument'])

    return instrument 