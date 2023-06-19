##########################
####   Unit Testing   ####
##########################

import pytest
from app import app
from flask import json

TEST_CLIENT = app.test_client()
__CONTENT_TYPE_JSON = 'application/json'

token = None

##########################
####   User Testing   ####
##########################

@pytest.mark.order(1)
def test_create_user():
  pyload = {
    "email": "bielgomesdasilva@hotmail.com",
    "password": "123456",
    "name": "Gabriel",
    "username": "bielgomesdasilva"
  }

  response = TEST_CLIENT.post('/users', content_type=__CONTENT_TYPE_JSON, data=json.dumps(pyload))
  assert response.status_code == 200

@pytest.mark.order(2)
def test_get_token():
  pyload = {
    "email": "bielgomesdasilva@hotmail.com",
    "password": "123456",
  }

  response = TEST_CLIENT.post('/users/token', content_type=__CONTENT_TYPE_JSON, data=json.dumps(pyload))
  data = json.loads(response.data)

  global token
  token = data['token']
 
  assert token != None
  assert response.status_code == 200

@pytest.mark.order(3)
def test_delete_user():
  response = TEST_CLIENT.delete('/users', headers={'Authorization': token})

  response_after_delete = TEST_CLIENT.get('/users')

  assert response.status_code == 200

##########################
####   Chat Testing   ####
##########################

def test_b():
  assert True

##########################
####  Message Testin  ####
##########################

def test_c():
  assert True