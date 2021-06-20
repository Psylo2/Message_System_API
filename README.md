# Message System API

Messaging System API
build with Python, Flask, Flask-RESTful,
Flask-JWT-Extended & Flask-SQLAlchemy

Deployed over Heroku
https://message-system-api.herokuapp.com/



** __Request Headers
Authorization
Bearer__

##__User__
- Client Registration
- User Login 
- User Logout 
- Refresh access token
- Change Password




###Client Registration
_Register a User by given name, email, password_

_password must have 1 Upper 1 Lower 4 Digits 2 Special_

endpoint: `/register`

````
{
    "username": {{user_name}},
    "password": {{user_password}},
    "email": {{user_email}}
}
````

###Client Login
_User Login by Given name\email and password_

__POST__

endpoint: `/login`

````
{
    "username_email": {{user_email}},
    "password": {{user_password}}
}
````


###Users Logout**
_User Logout and Revoke exists token_

__POST__

endpoint: `/logout`


###Refresh Access Token**
_Refresh Access Token with Fresh Token_

__GET__

endpoint: `/refresh`


###Forgot Password
_Change Users Password by given name, email, new password and re-password_

__POST__

endpoint: /forgot_password

````
{
    "name": {{user_name}},
    "email": {{user_email}},
    "new_password": "AAaa1111@!",
    "re-password": "AAaa1111@!"
}
````

##Message
- Send a Message
- Read a Message
- All Unread Messages
- All Read Messages
- All Sent Messages
- All Received messages
- All Messages that have been read by receivers
###Send a Message**
_Send a Message_

__POST__

endpoint: `/msg/send`
````
{
  "send_to": "enter user name",
  "title": "msg Title",
  "body": "msg Body"
}
````

###Read a Message**
_Read a Message_

__GET__

endpoint: `/msg/id=<int:msg_id>`

###All Unread Messages**
_Display all Titles of unread Messages_

__GET__

endpoint: `/msg/all_unread`

###All Read Messages**
_Display all Titles of read Messages_

__GET__

endpoint: `/msg/all_read`

###All Sent Messages**

_Display all Titles of sent Messages_

__GET__

endpoint: `/msg/all_sent`

###All Received Messages**

_Display all Titles of received Messages_

__GET__

endpoint: `/msg/all_received`

###All Been Read Messages by others**
_Display all Titles of messages that have been read by receivers_

__GET__

endpoint: `/msg/all_receivers_read`

##Admin
- Display Users List
- Display Logs

##All Users List**

_[__Admin only__] Display all Users without email and password_

__GET__

endpoint: `\admin_users_list`

##Log
- Display all Logs
- Search a Log by ID
- Search Log by threat level
- search all Logs of a user by user ID
- search all Logs of a user and threat level
- 

###Display All Logs**
_[__Admin only__] Display all Logs_

__GET__

endpoint: `/logs/all`


###Search by Log ID**
_[__Admin only__] Display a Log by id_

__POST__

endpoint: `/logs/id=<int:log_id>`

###Search by Threat level**

_[__Admin only__] Display a Log by id_

__POST__

_[__Admin only__] Display all Logs by given threat level ['H', 'M', 'L']_

endpoint: `/logs/level=<string:lvl>`

###Search by User ID**

_[__Admin only__] Display all Logs of a user_

__POST__


endpoint: `/logs/user=<int:user_id>`


###Search by User & Threat Level**

_[__Admin only__] Display all logs by user id and threat level ['H', 'M', 'L']_

__POST__

endpoint: `/logs/id=<int:user_id>&level=<string:lvl>`

