##
 # This file is used to soloy connect to MySQL and make changes to the database
 ##
from flask import Flask, render_template, json, url_for
# Importing a MySQL helper
import pymysql

# Opens mysql.json file to grab mySQL super secret data
with open("config/mysql.json") as json_file:
    json_data = json.load(json_file)

##
 # Connecting to mySQL with username/password (in .config file)
 # Connect using mysql -u root -p (Must have mysql downloaded)
 ##
db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
def update():
    print('yesdfea');
