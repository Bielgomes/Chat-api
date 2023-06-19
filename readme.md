# Endpoints

## User

### Create

`POST /users`

### Get Token

`POST /users/token`

### Upload Avatar

`POST /users/avatar`

### Download Avatar

`GET /users/<int:user_id>/avatar`

### Get User

`GET /users/<int:user_id>`

### Get Chats

`GET /users/chats`

### Update User

`PATCH /users`
`PATCH /users/email`
`PATCH /users/password`



## Chat

### Create

`POST /chats`

### Get

`GET /chats/<int:chat_id>`

### Get Users

`GET /chats/<int:chat_id>/users`

### Update

`PUT /chats/<int:chat_id>`

### Add User to Chat

`POST /chats/<int:chat_id>/join`

### Delete

`DELETE /chats/<int:chat_id>`

### Remove User from Chat

`REMOVE /chats/<int:chat_id>/leave`

### Admin Remove User from Chat

`REMOVE /chats/<int:chat_id>/admin/users/<int:user_id>`



## Message

### Create

`POST /chats/<int:chat_id>/messages`

### Get

`GET /chats/<int:chat_id>/messages?userid=<int:userid>&text=<str:text>`

### Delete

`DELETE /chats/<int:chat_id>/messages/<int:message_id>`