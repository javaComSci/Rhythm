# python -m unittest test_flaskr

import json
import unittest

from app import app
# set our application to testing mode
app.testing = True
idd = None;


class TestApi(unittest.TestCase):
    #
     # Test: Will register a user by the email 'dellamoresteven@gmail.com'
     # assert -> Check for a 'true' return
     #
    # def test_A_RegisterAccount(self):
    #     with app.test_client() as client:
    #         response=client.post('/register',
    #                    data=json.dumps(dict(email='dellamoresteven@gmail.com')),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         assert "true" == json_data['ok']
    #
    # ##
    #  # Test: Try to register another user by the email 'dellamoresteven@gmail.com'
    #  # assert -> Check for a 'false' return
    #  ##
    # def test_A__RegisterAccount(self):
    #     with app.test_client() as client:
    #         response=client.post('/register',
    #                    data=json.dumps(dict(email='dellamoresteven@gmail.com')),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         assert "false" == json_data['ok']
    #         print(json_data['ok'])
    #
    # ##
    #  # Test: Get the ID of the newly registered email
    #  # assert -> Make sure that the return value is a number
    #  ##
    # def test_B_CheckDataBaseForInsertion(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/getInfoByEmail',
    #                    data=json.dumps(dict(table="user", email="dellamoresteven@gmail.com")),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         idd = json_data[0][0];
    #         print("idd = {}".format(idd))
    #         assert type(idd) == type(1)
    #
    # ##
    #  # Test: Adds the composition for the user
    #  # assert -> Checks to make sure the composition is added
    #  ##
    # def test_C_AddComposition(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/newComposition',
    #                    data=json.dumps(dict(id=idd, description="JesusTest", name="JesusCompoTest")),
    #                    content_type='application/json')
    #         print(response.data)
    #         assert "newCompoAdded" == response.data
    #
    # ##
    #  # Test: Tried to update the composition name
    #  # assert -> Check to make sure we were returned a valid response
    #  ##
    # def test_D_TestUpdate(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/update',
    #                    data=json.dumps(dict(table="composition", update=["name", "ChangedName"], where=["user_id", idd])),
    #                    content_type='application/json')
    #         print(response.data)
    #         assert "updated" == response.data
    #
    # ##
    #  # Test: To check updated composition name
    #  # assert -> Checks to make sure the name has been changed and reflected
    #  #           in the database
    #  ##
    # def test_E_getInfoOnComosition(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/getInfo',
    #                    data=json.dumps(dict(table="composition", id=idd)),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         print(json_data)
    #         assert type(json_data[0][0]) ==  type(1)
    #         assert json_data[0][1] == "ChangedName"
    #         assert json_data[0][2] == "JesusTest"
    #         assert json_data[0][3] == idd
    #
    # ##
    #  # Test: Add a new newMusicSheet
    #  # assert -> Make sure the server response is true
    #  ##
    # def test_F_AddMusicSheet(self):
    #     print("1")
    #     # global idd
    #     # with app.test_client() as client:
    #     #     response=client.post('/getInfo',
    #     #                data=json.dumps(dict(table='composition', id=idd)),
    #     #                content_type='application/json')
    #     #     json_data = json.loads(response.data)
    #     #     compID = json_data[0][0];
    #     #
    #     # with app.test_client() as client:
    #     #     response=client.post('/newMusicSheet',
    #     #                data=json.dumps(dict(comp_id=compID, name="TestMusicSheet")),
    #     #                content_type='application/json')
    #     #     json_data = json.loads(response.data)
    #
    # ##
    #  # Test: Delete a Music sheet
    #  # assert -> Make sure the server response is true
    #  ##
    # def test_G_DeleteMusicSheet(self):
    #     print("1")
    #     # print("FEWAFEWSGJSERAJGAEQ")
    #     # global idd
    #     # with app.test_client() as client:
    #     #     response=client.post('/getInfo',
    #     #                data=json.dumps(dict(table='composition', id=idd)),
    #     #                content_type='application/json')
    #     #     json_data = json.loads(response.data)
    #     #     compIDD = json_data[0][0];
    #     #
    #     # with app.test_client() as client:
    #     #     response=client.post('/delete',
    #     #                data=json.dumps(dict(table='sheet_music', delete=["composition_id", compIDD])),
    #     #                content_type='application/json')
    #     #     json_data = json.loads(response.data)
    #         # assert "true" == json_data['ok']
    #         # compID = json_data[0][1];
    #
    # ##
    #  # Test: To check if you can delete a composition
    #  # assert -> Checks to make sure the return value is true
    #  ##
    # def test_H_DeleteCompositions(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/delete',
    #                    data=json.dumps(dict(table='composition', delete=['user_id', idd])),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         assert "true" == json_data['ok']
    #
    # ##
    #  # Test: Tried to recover an account, then gets the Verf id code
    #  # assert -> Make sure the email was sent to 'dellamoresteven@gmail.com'
    #  # assert -> Make sure the verf code was correct
    #  # assert -> Make sure the verf_code has been reset in the databse
    #  ##
    # def test_I_EmailSender(self):
    #     global idd
    #     with app.test_client() as client:
    #         response=client.post('/recoverEmail',
    #                    data=json.dumps(dict(email='dellamoresteven@gmail.com')),
    #                    content_type='application/json')
    #         assert response.data == "sent"
    #
    #     with app.test_client() as client:
    #         response=client.post('/getInfo',
    #                    data=json.dumps(dict(table='user', id=idd)),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         # print("HERE {}".format(json_data[0][2]))
    #         verCode = json_data[0][2]
    #
    #     with app.test_client() as client:
    #         response=client.post('/checkKey',
    #                    data=json.dumps(dict(code=verCode)),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         print("HERE {}".format(json_data))
    #         assert json_data['ok'] == "true"
    #         assert json_data['id'] == idd
    #
    #     with app.test_client() as client:
    #         response=client.post('/getInfo',
    #                    data=json.dumps(dict(table='user', id=idd)),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         # print("HERE {}".format(json_data[0][2]))
    #         assert -1 == json_data[0][2]

    ##
     # Test: Delete an Account
     # Assert -> Make sure a true was sent back
     ##
    # def test_Z_DeleteAccount(self):
    #     with app.test_client() as client:
    #         response=client.post('/delete',
    #                    data=json.dumps(dict(table='user', delete=['email', "dellamoresteven@gmail.com"])),
    #                    content_type='application/json')
    #         json_data = json.loads(response.data)
    #         assert "true" == json_data['ok']
