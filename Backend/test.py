from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)



@app.route("/")
def index():


if __name__ == '__main__':
   app.run(debug = True)
