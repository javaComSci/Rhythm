# python -m unittest test_flaskr3

import json
import unittest

from app import app
# set our application to testing mode
app.testing = True
idd = None;


class TestApi(unittest.TestCase):

  def test_A_selectInstrument(self):
      with app.test_client() as client:
          response=client.post('/selectInstrument',
                     data=json.dumps(dict(sheet_id=247, instrument='Violin')),
                     content_type='application/json')
          if not isinstance(response.data, str): 
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Violin'

  def test_B_selectInstrument(self):
      with app.test_client() as client:
          response=client.post('/selectInstrument',
                     data=json.dumps(dict(sheet_id=247, instrument='NONEXISTANTINSTRUMENT')),
                     content_type='application/json')
          if not isinstance(response.data, str): 
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Piano'

  def test_C_selectInstrument(self):
      with app.test_client() as client:
          response=client.post('/selectInstrument',
                     data=json.dumps(dict(sheet_id=247, instrument=65456)),
                     content_type='application/json')
          if not isinstance(response.data, str): 
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'false'

  def test_D_exportPDF(self):
      with app.test_client() as client:
          response=client.post('/createPDF',
                     data=json.dumps(dict(sheet_ids=['222'], email='iramanat@purdue.edu')),
                     content_type='application/json')
          if not isinstance(response.data, str): 
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Sent All Successfully'

  def test_E_exportPDF(self):
      with app.test_client() as client:
          response=client.post('/createPDF',
                     data=json.dumps(dict(sheet_ids=['89090'], email='iramanat@purdue.edu')),
                     content_type='application/json')
          if not isinstance(response.data, str): 
            decodedData = response.data.decode('utf-8')
          else:
            decodedData = response.data
          assert decodedData == 'Some Sheets Missing'

