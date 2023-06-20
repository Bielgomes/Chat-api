##########################
####   Unit Testing   ####
##########################

import pytest
from app import app
from flask import json

TEST_CLIENT = app.test_client()
__CONTENT_TYPE_JSON = 'application/json'

token = None
tmp_token = None
new_token = None

##########################
####   User Testing   ####
##########################

@pytest.mark.order(1)
def test_create_user():
  payload = {
    "email": "bielgomesdasilvaTESTE@hotmail.com",
    "password": "123456",
    "name": "Gabriel",
    "description": "bielgomesdasilva"
  }

  response = TEST_CLIENT.post('/users', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  assert response.status_code == 200

@pytest.mark.order(2)
def test_get_token():
  payload = {
    "email": "bielgomesdasilvaTESTE@hotmail.com",
    "password": "123456",
  }

  response = TEST_CLIENT.post('/users/token', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  data = json.loads(response.data.decode('utf-8'))

  global token
  token = data['token']
 
  assert token != None
  assert response.status_code == 200

@pytest.mark.order(3)
def test_get_user_by_token():
  response = TEST_CLIENT.get('/users', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert data['id']
  assert data['name']
  assert data['description']

@pytest.mark.order(4)
def test_get_user_by_id():
  response = TEST_CLIENT.get('/users', headers={'Authorization': token})
  user = json.loads(response.data.decode('utf-8'))

  response = TEST_CLIENT.get(f'/users/{user["id"]}')
  data = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert user['id'] == data['id']
  assert user['name'] == data['name']
  assert user['description'] == data['description']

@pytest.mark.order(5)
def test_upload_avatar():
  avatar = open('tmp/test_avatar.jpg', 'rb')
  response = TEST_CLIENT.post('/users/avatar', headers={'Authorization': token}, content_type='multipart/form-data', data={'file': avatar})

  avatar.close()

  assert response.status_code == 200

@pytest.mark.order(6)
def test_get_avatar():
  response = TEST_CLIENT.get('/users', headers={'Authorization': token})
  user = json.loads(response.data.decode('utf-8'))

  response = TEST_CLIENT.get(f'/users/{user["id"]}/avatar')
  data = response.data

  assert response.status_code == 200
  assert data

@pytest.mark.order(8)
def test_get_chats():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(data) == 1

@pytest.mark.order(19)
def test_update_info_user():
  payload = {
    "name": "Bielgomes",
    "description": "..."
  }

  response = TEST_CLIENT.get('/users', headers={'Authorization': token})
  user = json.loads(response.data.decode('utf-8'))

  response_ = TEST_CLIENT.patch('/users', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  
  response = TEST_CLIENT.get('/users', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  assert response_.status_code == 200
  assert user['name'] != data['name']
  assert user['description'] != data['description']

@pytest.mark.order(20)
def test_update_email_user():
  payload = {
    "email": "bielgomesTESTE@hotmail.com",
  }

  payload_ = {
    "email": "bielgomesTESTE@hotmail.com",
    "password": "123456",
  }

  TEST_CLIENT.patch('/users/email', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  response = TEST_CLIENT.post('/users/token', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload_))

  assert response.status_code == 200

@pytest.mark.order(21)
def test_update_password_user():
  payload = {
    "password": "157359",
  }

  payload_ = {
    "email": "bielgomesTESTE@hotmail.com",
    "password": "157359",
  }

  TEST_CLIENT.patch('/users/password', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  response = TEST_CLIENT.post('/users/token', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload_))
  data = json.loads(response.data.decode('utf-8'))

  global new_token
  new_token = data['token']

  assert response.status_code == 200
  assert new_token != token

@pytest.mark.order(22)
def test_delete_users():
  payload = {
    "email": "bielgomesTESTE@hotmail.com",
    "password": "157359",
  }

  payload_ = {
    "email": "testeuser@hotmail.com",
    "password": "157359",
  }

  TEST_CLIENT.delete('/users', headers={'Authorization': new_token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  TEST_CLIENT.delete('/users', headers={'Authorization': tmp_token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload_))
  response = TEST_CLIENT.get('/users', headers={'Authorization': new_token})

  assert response.status_code == 404

##########################
####   Chat Testing   ####
##########################

@pytest.mark.order(7)
def test_create_chat():
  payload = {
    "name": "Chat Teste",
    "description": "Chat de teste",
    "max_users": 10
  }

  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  chats = json.loads(response.data.decode('utf-8'))

  response = TEST_CLIENT.post('/chats', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

  new_response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  new_chats = json.loads(new_response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(chats) < len(new_chats)

@pytest.mark.order(9)
def test_get_chat_by_id():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.get(f'/chats/{chat_id}', headers={'Authorization': token})
  chats = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert chats['id'] == chat_id

@pytest.mark.order(10)
def test_get_chat_users():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.get(f'/chats/{chat_id}/users', headers={'Authorization': token})
  chat_users = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(chat_users) == 1

@pytest.mark.order(11)
def test_update_chat():
  payload = {
    "name": "Chat Teste TESTE",
    "description": "Chat de teste TESTE",
    "max_users": 20
  }

  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat = data[-1]

  response = TEST_CLIENT.put(f'/chats/{chat["id"]}', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

  new_response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  new_data = json.loads(new_response.data.decode('utf-8'))

  new_chat = new_data[-1]

  assert response.status_code == 200
  assert chat['name'] != new_chat['name']
  assert chat['description'] != new_chat['description']
  assert chat['max_users'] != new_chat['max_users']

@pytest.mark.order(12)
def test_join_chat():
  payload = {
    "email": "testeuser@hotmail.com",
    "password": "157359",
    "name": "Teste User",
    "description": "Teste User"
  }

  TEST_CLIENT.post('/users', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  response = TEST_CLIENT.post('/users/token', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))
  data = json.loads(response.data.decode('utf-8'))

  global tmp_token
  tmp_token = data['token']

  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.post(f'/chats/{chat_id}/join', headers={'Authorization': tmp_token})

  assert response.status_code == 200

@pytest.mark.order(13)
def test_leave_chat():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': tmp_token})
  chats = json.loads(response.data.decode('utf-8'))

  chat_id = chats[-1]['id']

  response = TEST_CLIENT.delete(f'/chats/{chat_id}/leave', headers={'Authorization': tmp_token})

  new_response = TEST_CLIENT.get('/users/chats', headers={'Authorization': tmp_token})
  new_chats = json.loads(new_response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(chats) > len(new_chats)

@pytest.mark.order(14)
def test_admin_expulse_user():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.post(f'/chats/{chat_id}/join', headers={'Authorization': tmp_token})

  response = TEST_CLIENT.get(f'/chats/{chat_id}/users', headers={'Authorization': token})
  chat_users = json.loads(response.data.decode('utf-8'))

  user_id = chat_users[-1]['id']

  response = TEST_CLIENT.delete(f'/chats/{chat_id}/admin/users/{user_id}', headers={'Authorization': token})

  new_response = TEST_CLIENT.get(f'/chats/{chat_id}/users', headers={'Authorization': token})
  new_chat_users = json.loads(new_response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(chat_users) > len(new_chat_users)

@pytest.mark.order(18)
def test_delete_chat():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  chats = json.loads(response.data.decode('utf-8'))

  chat_id = chats[-1]['id']

  response = TEST_CLIENT.delete(f'/chats/{chat_id}', headers={'Authorization': token})

  new_response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  new_chats = json.loads(new_response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(chats) > len(new_chats)

###########################
####  Message Testing  ####
###########################

@pytest.mark.order(15)
def test_create_message():
  payload = {
    "message": "Teste de mensagem"
  }

  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.post(f'/chats/{chat_id}/messages', headers={'Authorization': token}, content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

  assert response.status_code == 200

@pytest.mark.order(16)
def test_get_messages():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.get(f'/chats/{chat_id}/messages', headers={'Authorization': token})
  messages = json.loads(response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(messages) > 0

@pytest.mark.order(17)
def test_delete_message():
  response = TEST_CLIENT.get('/users/chats', headers={'Authorization': token})
  data = json.loads(response.data.decode('utf-8'))

  chat_id = data[-1]['id']

  response = TEST_CLIENT.get(f'/chats/{chat_id}/messages', headers={'Authorization': token})
  messages = json.loads(response.data.decode('utf-8'))

  message_id = messages[-1]['id']

  response = TEST_CLIENT.delete(f'/chats/{chat_id}/messages/{message_id}', headers={'Authorization': token})

  new_response = TEST_CLIENT.get(f'/chats/{chat_id}/messages', headers={'Authorization': token})
  new_messages = json.loads(new_response.data.decode('utf-8'))

  assert response.status_code == 200
  assert len(messages) > len(new_messages)