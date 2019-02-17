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
from flask import Flask, render_template, json, url_for, request

# Grabbing the connection file
from user import users
from user import deleteUser
import user.routes.delete as deletes
import user.routes.delete as recoverAccounts
import user.routes.delete as updates
import user.routes.delete as uploadImages

##
 # Creates an instance of the exisiting class/module
 # __name__ is the name of the module I beleive
 ##
app = Flask(__name__)

##
 # Registers a new user
 ##
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        return users.registerRoute()
    else:
        return '\n\nShould not see this: app.py\n\n'

##
 # Deletes information on a specific user
 ##
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        return deletes.deleteRoute()
    else:
        return '\n\nShould not see this: app.py\n\n'

##
 # Deletes a user (This really just puts the user into ghost mode)
 ##
# @app.route('/deleteUser', methods=['POST'])
# def delete():
    # if request.method == 'POST':
    #     # return deleteUser.deleteUsers()
    # else:
    #     return '\n\nShould not see this: app.py\n\n'

##
 # This runs the server with debug=on so we can see outputs in the terminal.
 # Simlar to nodemon, it refreshes when you save! Yay!
 ##
if __name__ == "__main__":
  app.run(debug=True)
