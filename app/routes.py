# app/routes.py
from flask import Blueprint, render_template, request, g, redirect, send_from_directory, current_app
from .module import auth, profile, tasks
from .user import userPage
from .authPage import authPage
import os

main = Blueprint('main', __name__, template_folder="html",static_folder='static',)

main.register_blueprint(userPage)
main.register_blueprint(authPage)

@main.before_app_request
def admin_middleware():
    if auth.validToken(request.cookies.get('sessionToken')):
        g.isAuthenticated = True
        g.token = request.cookies.get('sessionToken')
    else:
        g.isAuthenticated = False

# # --- 1. THE REACT LOADER ---
# # This route serves the actual React application
# @main.route('/', defaults={'path': ''})
# @main.route('/<path:path>')
# def serve(path):
#     # 1. Look for the file in the static folder (e.g., assets/index.js)
#     if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
#         return send_from_directory(current_app.static_folder, path)
    
#     # 2. If the file doesn't exist (like a React route /dashboard), serve index.html
#     return send_from_directory(current_app.static_folder, 'index.html')


@main.route('/')
def index():
    featured = tasks.getFeatured()
    print(featured)
    return render_template("index.html",lessons=featured)

@main.route('/soon')
def soon():
    return render_template("comming_soon.html")



