from flask_login import login_user, logout_user
from flask import request, jsonify
from flask_restful import Resource, reqparse
import bcrypt
from config import login_manager
from db import db

Users = db["Users"]

parser = reqparse.RequestParser()

class User():
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

def verifyPassword(username, password):
    hashed_pwd = Users.find_one({
        "username": username
    })["password"]

    if bcrypt.checkpw(password.encode("utf8"), hashed_pwd):
        return True
    else:
        return False

@login_manager.user_loader
def load_user(username):
    user = Users.find_one({
        "username": username
    })
    if not user:
        return None
    return User(user['username'])

@login_manager.unauthorized_handler
def unauthorized():
    retJson = {
        "message": "Unauthorized request",
        "status": 401
    }
    return jsonify(retJson)

def userExists(username):
    user = Users.find_one({
        "username": username
    })
    if user is not None:
        return True
    else:
        return False

def getUser(username):
    user = Users.find_one({
        "username": username
    })
    return user

class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            if userExists(username):
                return jsonify({
                    'message': 'User with username "{}" already exist!'.format(username)
                })

            hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

            Users.insert_one({
                "username": username,
                "password": hashed_pw,
                "is_active": False
            })

            retJson = {
                "message": "User registered successfully",
                "status": 201
            }
            return jsonify(retJson)
        except Exception as err:
            retJson = {
                "status": 500,
                "message": "err"
            }
            return jsonify(retJson)

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if not userExists(username):
            return jsonify({'message': 'User {} doesn\'t exist'.format(username)})
        correct_pswd = verifyPassword(username, password)
        if correct_pswd:
            obj = User(username)
            login_user(obj)
            retJson = {
                "message": "Successfully logged in!"
            }
            return jsonify(retJson)
        else:
            return jsonify({'message': 'Wrong credentials'})

class Logout(Resource):
    def get(self):
        logout_user()
        retJson = {
            "message": "User logged out successfully",
            "status": 200
        }
        return jsonify(retJson)