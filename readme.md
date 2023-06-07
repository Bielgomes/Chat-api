# Endpoints

## User

### Create

`POST /users`

### Get Token

`POST /users/token`

### Get User

`GET /users`

### Update User

`PATCH /users`
`PATCH /users/email`
`PATCH /users/password`



## Chat

### Create

`POST /chats`

### Get

`GET /chats/<int:chat_id>`

### Update

`PUT /chats/<int:chat_id>`

### Delete

`DELETE /chats/<int:chat_id>`

### Add User

`POST /chats/<int:chat_id>/join`



## Message

### Create

`POST /chats/<int:chat_id>/messages`

### Get

`GET /chats/<int:chat_id>/messages?filter`

### Delete

`DELETE /chats/<int:chat_id>/messages/<int:message_id>`