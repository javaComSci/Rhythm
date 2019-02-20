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
from flask import Flask, url_for

app = Flask(__name__)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/register")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "POST" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
