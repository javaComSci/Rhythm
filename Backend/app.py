##
 # Notes:
 # 1. This langauge is alright...
 # 2. Make sure to run this on local host to test right now!
 # 3. Were gonna need to pass some type of token so that people
 #    cant run our routes from the browser
 # 4. source Backend/bin/activate to get into the Virtual Env
 # 5. pip install -r requirements.txt to install requirements.txt
 #
 #    Steve The Great IV.
 ##

# Importing Flask, from flask, Also render_template
from flask import Flask, render_template

##
 # Creates an instance of the exisiting class? I THINK
 # Who really knows???????????????
 # __name__ is the name of the class i beleive
 ##
app = Flask(__name__)

##
 # Create a new route with the @app.route tag
 # (def)ine a function, home, that will be mapped to '/' route
 ##
@app.route("/")
def home():
  return "This language is bullshit!"

# Something like this can work if we need to send a html file over
  # return render_template('home.html')

##
 # Create a new route with the @app.route tag
 # (def)ine a function, nothello, that will be mapped to '/PythonSucks' route
 ##
@app.route("/PythonSucks")
def nothello():
    return "This language is bullshit123!"

##
 # This runs the server with debug=on so we can see outputs in the terminal.
 # Simlar to nodemon, it refreshes when you save! Yay!
 ##
if __name__ == "__main__":
  app.run(debug=True)
