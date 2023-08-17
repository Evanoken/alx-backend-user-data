## Session Authentication

### Description
This repository contains the code and resources for learning about session authentication.

**Session authentication** is a way to authenticate users by storing their information on the server. This is in contrast to basic authentication, where the user's information is stored on the client side.

### Topics Covered

- **Session authentication** - We learn about session authentication, and how to use it to authenticate users.

- **Cookies** - We learn about cookies, and how to use them to store information on the client side.

- **Flask Cookies** - We learn about the `request` and `make_response` modules in Flask, and how to use them to set and get cookies.

## Simple API

Simple HTTP API for playing with `User` model.


### Files

#### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

#### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


### Setup

```
$ pip3 install -r requirements.txt
```


### Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


### Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)


### Resources

- [Sessions](https://developer.mozilla.org/en-US/docs/Web/HTTP/Session)
- [HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [Flask Cookies](https://flask.palletsprojects.com/en/1.1.x/quickstart/#cookies)