from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # update calls MySQLConnect.py update function to update a specific value
 ##
def update():
    content = request.json
    print("update Route Call")
    # results = MySQLConnect.update(content['table'], content['id'], );
    return 'updated'
