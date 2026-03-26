# app/apis/userWebPage.py
from flask import Blueprint, g, jsonify, url_for, redirect, request
api_user = Blueprint('api_user', __name__, url_prefix="/user")
from ..module import auth, profile
from functools import wraps

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.isAuthenticated:
            return {}, 401
        return func(*args, **kwargs)
    return wrapper

@api_user.route('/<int:id>/profile')
@auth_required
def getUserData(id):
    try:
        user = profile.userById(id)
        return user.getPublic()
    except profile.UserNotFoundError:
        return {"not found"}, 404



@api_user.route("/header")
def userdata():
    try:
        user = auth.getUserFromToken(g.get("token"))
    except profile.UserNotFoundError:
        return {"error":"Forbidden"}, 403
    user = profile.userById(1)
    data = {
        "username": user.username,
        "xp": user.xp,
    }
    return jsonify(data)

@api_user.route("/search")
@auth_required
def searchUser():
    username = request.args.get("username","")
    try:
        users = profile.searchUserByUsername(username)
    except profile.UserNotFoundError:
        return {}, 403
    return users # jsonify(user.getPublic())
