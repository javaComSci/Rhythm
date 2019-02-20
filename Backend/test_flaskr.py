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


class TestApi(unittest.TestCase):

    def test_main(self):
        with app.test_client() as client:
            response=client.post('/register', 
                       data=json.dumps(dict(email='asdf')),
                       content_type='application/json')
            # check result from server with expected data

            self.assertEqual(
                response.data,
                json.dumps(response)
            )