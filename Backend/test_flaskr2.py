# python -m unittest test_flaskr2

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
                       data=json.dumps(dict(email='dellamoresteven@gmail.com')),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "false" == json_data['ok']

    def test_B_RegisterAccount(self):
        with app.test_client() as client:
            response=client.post('/register',
                       data=json.dumps(dict(email='PizzaMan205@gmail.com')),
                       content_type='application/json')
            json_data = json.loads(response.data)
            assert "true" == json_data['ok']

    def test_C_duplicateSheet(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=0, sheet_id=0)),
                       content_type='application/json')
            assert response.data == "duplicateSheet"

    def test_D_duplicateSheet1(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=-10, sheet_id=10)),
                       content_type='application/json')
            assert response.data == "false"
            with app.test_client() as client:
                response=client.post('/duplicateSheet',
                           data=json.dumps(dict(comp_id=-100, sheet_id=10)),
                           content_type='application/json')
                assert response.data == "false"

    def test_E_duplicateSheet2(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=15, sheet_id=-7)),
                       content_type='application/json')
            assert response.data == "false"
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=15, sheet_id=-17)),
                       content_type='application/json')
            assert response.data == "false"

    def test_F_duplicateSheet3(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=-5, sheet_id=-3)),
                       content_type='application/json')
            assert response.data == "false"
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=-9, sheet_id=-1)),
                       content_type='application/json')
            assert response.data == "false"

    def test_G_duplicateSheet4(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=10000, sheet_id=33)),
                       content_type='application/json')
            assert response.data == "false"
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=10000, sheet_id=333)),
                       content_type='application/json')
            assert response.data == "false"

    def test_H_duplicateSheet5(self):
        with app.test_client() as client:
            response=client.post('/duplicateSheet',
                       data=json.dumps(dict(comp_id=0, sheet_id=30030)),
                       content_type='application/json')
            assert response.data == "false"

    def test_I_duplicateCompo1(self):
        with app.test_client() as client:
            response=client.post('/duplicateComposition',
                       data=json.dumps(dict(comp_id=146, title="Spoon Symphony", user_id=231)),
                       content_type='application/json')
            assert response.data == "duplicatedComposition"

    def test_J_duplicateCompo2(self):
        with app.test_client() as client:
            response=client.post('/duplicateComposition',
                       data=json.dumps(dict(comp_id=146, title="NotARealCompo", user_id=231)),
                       content_type='application/json')
            assert response.data == "false"

    def test_K_duplicateCompo3(self):
        with app.test_client() as client:
            response=client.post('/duplicateComposition',
                       data=json.dumps(dict(comp_id=146, title="Spoon Symphony", user_id=1001)),
                       content_type='application/json')
            assert response.data == "false"

    def test_L_duplicateCompo4(self):
        with app.test_client() as client:
            response=client.post('/duplicateComposition',
                       data=json.dumps(dict(comp_id=1001, title="Spoon Symphony", user_id=231)),
                       content_type='application/json')
            assert response.data == "false"
