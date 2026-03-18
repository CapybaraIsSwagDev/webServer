# app/api.py
from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
api = Blueprint('api', __name__, url_prefix="/api")
from ..module import auth
from .api_user import api_user
from .api_auth import api_auth

api.register_blueprint(api_user)
api.register_blueprint(api_auth)

@api.errorhandler(404)
def not_found(e):
    return jsonify({"error":"Invalid Url"}), 404

@api.before_app_request
def admin_middleware():
    if not request.path.startswith("/api"):
        return

    if not auth.validToken(request.cookies.get('sessionToken')):
        g.isAuthenticated = False
    else:
        g.isAuthenticated = True
        g.token = request.cookies.get('sessionToken')

@api.route('/')
def main():
    return jsonify({"error":"Invalid Request","message":"Welcome :)"}), 404
