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

    def test_K_sendingImageExtended(self):
      with app.test_client() as client:
          response=client.post('/uploadImage',
                     data=json.dumps(dict(img_data='ka09', compID=1231, final=False, boxHeight=70, boxWidth=500, X=0, Y=0)),
                     content_type='application/json')
          if not isinstance(response.data, str):
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Not valid sheet id'

          response=client.post('/uploadImage',
                     data=json.dumps(dict(img_data='ka09', compID=1231, final=True, boxHeight=70, boxWidth=500, X=0, Y=0)),
                     content_type='application/json')
          if not isinstance(response.data, str):
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Not valid sheet id'

    def test_L_sendingImageExtended(self):
      with app.test_client() as client:
          response=client.post('/uploadImage',
                     data=json.dumps(dict(sheetID=90112, compID=1231, boxHeight=70, boxWidth=50, final=True, X=0, Y=0)),
                     content_type='application/json')
          if not isinstance(response.data, str):
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'No image given'

    def test_M_sendingImageExtended(self):
      with app.test_client() as client:
          response=client.post('/setAuthor',
                     data=json.dumps(dict(author = "Steven", sheet_id= 248)),
                     content_type='application/json')
          if not isinstance(response.data, str):
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'updateAuthor'

    def test_N_ChangeTemp(self):
      with app.test_client() as client:
          response=client.post('/setTempo',
                     data=json.dumps(dict(tempo= 11, sheet_id= 248)),
                     content_type='application/json')
          if not isinstance(response.data, str):
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'updateTempo'
