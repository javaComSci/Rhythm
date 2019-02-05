##
 # Steps to make this thing run:
 # 1. export FLASK_APP=app.py => Ran in Backend/ => This will make it so you
 #    auto connect to the Virtual box/container
 # 2. pip install -r requirements.txt => This downloads all the dependencies
 # 3. Go check out the google docs folder and make sure you have Backend/config/mysql.json file
 # 4. Flask run => This should start up the server... maybe..
 # Note: I dont know if you need mysql downloaded since it is being run of a AWS instance, but
 # if you run into problems try to download mySQL.
 # Test: To make sure its running type localhost:5000/ into your browser!
 ##

# Importing Flask dependencies
from flask import Flask, render_template, json, url_for

# Opens mysql.json file to grab mySQL super secret data
with open("config/mysql.json") as json_file:
    json_data = json.load(json_file)

# Importing a MySQL helper
import pymysql

##
 # Connecting to mySQL with username/password (in .config file)
 # Connect using mysql -u root -p (Must have mysql downloaded)
 ##
db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")

##
 # Creates an instance of the exisiting class/module
 # __name__ is the name of the module I beleive
 ##
app = Flask(__name__)

##
 # Create a new route with the @app.route tag
 # (def)ine a function, home, that will be mapped to '/' route
 ##
@app.route("/")
def home():
    return "This language is really fun..!"

# Something like this can work if we need to send a html file over
  # return render_template('home.html')

##
 # Create a new route with the @app.route tag
 # (def)ine a function, nothello, that will be mapped to '/PythonSucks' route
 ##
@app.route("/testRoute")
def nothello():
    return ":(((())))"

##
 # This runs the server with debug=on so we can see outputs in the terminal.
 # Simlar to nodemon, it refreshes when you save! Yay!
 ##
if __name__ == "__main__":
  app.run(debug=True)
