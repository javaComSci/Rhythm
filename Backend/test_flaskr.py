# import os
# import tempfile

# import pytest

# from flaskr import flaskr


# @pytest.fixture
# def client():
#     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#     flaskr.app.config['TESTING'] = True
#     client = flaskr.app.test_client()

#     with flaskr.app.app_context():
#         flaskr.init_db()

#     yield client

#     os.close(db_fd)
#     os.unlink(flaskr.app.config['DATABASE'])

import json
import unittest

from app import app
# set our application to testing mode
app.testing = True
idd = None;


class TestApi(unittest.TestCase):
    def test_A_RegisterAccount(self):
        with app.test_client() as client:
            response=client.post('/register',
                       data=json.dumps(dict(email='jesus@jesus.com')),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "true" == json_data['ok']
            print(json_data['ok'])

    def test_A__RegisterAccount(self):
        with app.test_client() as client:
            response=client.post('/register',
                       data=json.dumps(dict(email='jesus@jesus.com')),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "false" == json_data['ok']
            print(json_data['ok'])

    def test_B_CheckDataBaseForInsertion(self):
        global idd
        with app.test_client() as client:
            response=client.post('/getInfoByEmail',
                       data=json.dumps(dict(table="user", email="jesus@jesus.com")),
                       content_type='application/json')
            # print("Fucl yes")
            json_data = json.loads(response.data)
            idd = json_data[0][0];
            print("idd = {}".format(idd))
            assert type(idd) == type(1)
            # print("FEAW")

    def test_C_AddComposition(self):
        global idd
        with app.test_client() as client:
            response=client.post('/newComposition',
                       data=json.dumps(dict(id=idd, description="JesusTest", name="JesusCompoTest")),
                       content_type='application/json')
            print(response.data)
            assert "newCompoAdded" == response.data
            # json_data = json.loads(response.data)
            # print(json_data)

    def test_D_TestUpdate(self):
        global idd
        with app.test_client() as client:
            response=client.post('/update',
                       data=json.dumps(dict(table="composition", update=["name", "ChangedName"], where=["user_id", idd])),
                       content_type='application/json')
            print("Fucl yes")
            print(response.data)
            assert "updated" == response.data


    def test_E_getInfoOnComosition(self):
        print("START")
        global idd
        with app.test_client() as client:
            response=client.post('/getInfo',
                       data=json.dumps(dict(table="composition", id=idd)),
                       content_type='application/json')
            json_data = json.loads(response.data)
            print(json_data)
            assert type(json_data[0][0]) ==  type(1)
            assert json_data[0][1] == "ChangedName"
            assert json_data[0][2] == "JesusTest"
            assert json_data[0][3] == idd

    def test_F_DeleteCompositions(self):
        global idd
        with app.test_client() as client:
            response=client.post('/delete',
                       data=json.dumps(dict(table='composition', delete=['user_id', idd])),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "true" == json_data['ok']

    def test_G_EmailSender(self):
        global idd
        with app.test_client() as client:
            response=client.post('/delete',
                       data=json.dumps(dict(table='composition', delete=['user_id', idd])),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "true" == json_data['ok']

    def test_Z_DeleteAccount(self):
        with app.test_client() as client:
            response=client.post('/delete',
                       data=json.dumps(dict(table='user', delete=['email', "jesus@jesus.com"])),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "true" == json_data['ok']
