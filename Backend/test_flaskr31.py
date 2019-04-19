# python -m unittest test_flaskr31

import json
import unittest
import os.path
from app import app
# set our application to testing mode
app.testing = True
idd = None;


class TestApi(unittest.TestCase):

    def test_H_MitiCreation(self):
        with app.test_client() as client:
            response=client.get('/getSong?sheetid=238',
                data=json.dumps(dict({"clef" : 0, "notes": [{"note": 4, "length": 1, "pitch": 0}]})),
                content_type='application/json')
            print("RepONSe dATA")
            # if not isinstance(response.data, float):
            #     decodedData = response.data.decode('utf-8')
            # else:
            #     decodedData = response.data
            assert os.path.isfile('/home/Rhythm/Backend/238.mid') == True

    def test_I_MitiCreation(self):
        with app.test_client() as client:
            response=client.get('/getSong?sheetid=1295912',
                data=json.dumps(dict({"clef" : 0, "notes": [{"note": 4, "length": 1, "pitch": 0}]})),
                content_type='application/json')
            print("RepONSe dATA")
            # if not isinstance(response.data, float):
            #     decodedData = response.data.decode('utf-8')
            # else:
            #     decodedData = response.data
            assert os.path.isfile('/home/Rhythm/Backend/1295912.mid') == False


    def test_J_MitiCreation(self):
        with app.test_client() as client:
            response=client.get('/getSong?sheetid=-1295912',
                data=json.dumps(dict({"clef" : 0, "notes": [{"note": 4, "length": 1, "pitch": 0}]})),
                content_type='application/json')
            print("RepONSe dATA")
            # if not isinstance(response.data, float):
            #     decodedData = response.data.decode('utf-8')
            # else:
            #     decodedData = response.data
            assert os.path.isfile('/home/Rhythm/Backend/1295912.mid') == False
