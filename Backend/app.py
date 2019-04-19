##i
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
# from user import deleteUser
import user.deleteUser as deleteUsers
import user.routes.delete as deletes
import user.routes.uploadImage as uploadImages
# import user.routes.newMusicSheet as newMusicSheets
import user.routes.update as updates
# import user.routes.delete as uploadImages
import user.routes.newComposition as newCompositions
import user.routes.newMusicSheet as newMusicSheets
import user.routes.AccountRecovery as AccountRecoverys
import user.routes.getInfo as getInfos
import user.routes.createPDF as createPDFs
import user.routes.selectInstrument as selectInstruments
import user.routes.camera as camerass
from flask_mail import Mail, Message
##
# Creates an instance of the exisiting class/module
# __name__ is the name of the module I beleive
##
app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'rhythmrecovery@gmail.com',
    "MAIL_PASSWORD": 'ouch09038888'
}

app.config.update(mail_settings)
mail = Mail(app)


##
# Registers a new user
# EXAMPLE json
# {
#     "email": "Steve@IsTheBest.com"
# }

##
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        return users.registerRoute()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

##
 # Deletes information on a specific user
 # EXAMPLE json
 # {
 #     "table": "composition",
 #     "id": "1",
 #     "delete": ["name", "MyFirstCompo"]
 # }
 ##


@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        return deletes.deleteRoute()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

##
 # Deletes a user (This really just puts the user into ghost mode)
 # NOT FUNCTIONAL
 ##


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    if request.method == 'POST':
        return deleteUsers.deleteUsers()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

##
 # Call this to create a new composition for a user
 # EXAMPLE json
  # {
        #     "id": "1",    <- User_id
        #     "description": "I Like pancakes",
        #     "name": "MyFirstCompo"
  # }
 ##


@app.route('/newComposition', methods=['POST'])
def newComposition():
    if request.method == 'POST':
        return newCompositions.newCompo()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/newMusicSheet', methods=['POST'])
def newMusicSheet():
    if request.method == 'POST':
        return newMusicSheets.newMusicSheets()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/duplicateSheet', methods=['POST'])
def duplicateSheet():
    if request.method == 'POST':
        return newMusicSheets.duplicateSheet()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


'''
duplicateComposition
takes:
"title" - title of duplicated composition
"user_id" - user's ID
"comp_id" - id of composition to be duplicated
'''


@app.route('/duplicateComposition', methods=['POST'])
def duplicateComposition():
    if request.method == 'POST':
        return newCompositions.duplicateComposition()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

##
 # Specifically takes in form data with keys file and sheet_id
 # Sets sheet_id blob to given file in form data
 # EXAMPLE
 # {
 #      "file": BINARY DATA HERE,
 #      "sheet_id": 147
 # }
##


@app.route('/addSheetFile', methods=['POST'])
def addSheetFile():
    if request.method == 'POST':
        return newMusicSheets.addSheetFile()
    else:
        return '\n\nDEBUG: Sollte das nicht sehen'

@app.route('/addSheetJSON', methods=['POST'])
def addSheetJSON():
    if request.method == 'POST':
        return newMusicSheets.addSheetJSON()
    else:
        return '\n\nDEBUG: Sollte das nicht sehen'

##
 # Call this to get info on a specific user from a specific table.
 # This will return a json array of the results
 # EXAMPLE json
 # {
 #     "id": "1",
 #     "table": "user"
 # }
 ##


@app.route('/getInfo', methods=['POST'])
def getInfo():
    if request.method == 'POST':
        return getInfos.getInfo()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/getInfoByEmail', methods=['POST'])
def getInfoByEmail():
    if request.method == 'POST':
        return getInfos.getInfoByEmail()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/getInfoBySheet', methods=['POST'])
def getInfoBySheet():
    if request.method == 'POST':
        return getInfos.getInfoSheet()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

@app.route('/getInfoBySheetID', methods=['POST'])
def getInfoBySheett():
    print("HOT HERER")
    if request.method == 'POST':
        return getInfos.getInfoSheetbyID()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

@app.route("/getSong", methods=["GET"])
def getSong():
    print 'get song route'
    if request.method == 'GET':
        print(request.args.get('sheetid'),"SHeet ID!!!")
        if (request.args.get('sheetid')):
            print("IN THE ARGUMENT",request.args.get('sheetid'))
            man = getInfos.getSong(request.args.get('sheetid'))
            print("man = ", man)
            return man
        if (request.args.get('compid')):
            return getInfos.getCompSong(request.args.get('compid'))
    else:
        return 'no'


##
 # Will update a specfic value in a table for a specific user
 # {
# 	"table": "composition",
# 	"update": ["description", "Chucken"],
# 	"where": ["composition_id", 2]
#  }
 ##
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        return updates.update()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/updateMulti', methods=['POST'])
def updateMulti():
    if request.method == 'POST':
        return updates.updateMulti()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

# {
# 	"email": "dellamoresteven@gmail.com"
# }
# UPDATE user SET verf_code=NULL WHERE email='Hhh';


@app.route('/recoverEmail', methods=['POST'])
def recoverEmail():
    return AccountRecoverys.AccountRecovery(mail)

# {
# 	"code": 92477971865
# }


# will send the pdf to the user
@app.route('/createPDF', methods=['POST'])
def createPDF():
    # print "CALLING TO PDF"
    return createPDFs.exportPDF(mail, app)




# will select instrument for sheet music
@app.route('/selectInstrument', methods=['POST'])
def selectInstrument():
    # print "Selected Instrument!"
    if request.method == 'POST':
        return selectInstruments.selectMusic()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/checkKey', methods=['POST'])
def checkKey():
    if request.method == 'POST':
        return AccountRecoverys.checkKey()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'


@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    print("IN PROCESS TO UPLOAD!")
    if request.method == 'POST':
        return uploadImages.cameraPipeline()
    else:
        return '\n\nDEBUG: Should not see this: app.py\n\n'

@app.route('/setAuthor', methods=['POST'])
def setAuthor():
    return newMusicSheets.updateAuthor()

@app.route('/setTempo', methods=['POST'])
def setTempo():
    return newMusicSheets.updateTempo()



##
 # This runs the server with debug=on so we can see outputs in the terminal.
 # Simlar to nodemon, it refreshes when you save! Yay!
 ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
