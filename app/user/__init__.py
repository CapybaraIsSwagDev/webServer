# app/user.py
from flask import Blueprint, render_template, request, redirect, url_for, g
userPage = Blueprint('user', __name__, url_prefix="/user")
from ..module import profile, auth

## Sub Pages
from .lesson import lessonPage
from .notes import notesPage
userPage.register_blueprint(notesPage)
userPage.register_blueprint(lessonPage)

# Check if user is Authenticated if not go to login screen
@userPage.before_app_request
def admin_middleware():
    if not request.path.startswith("/user"):
        return
    
    current_url = request.full_path # destinatiojn
    if not g.isAuthenticated:
        return redirect(url_for("main.auth.login",dest=current_url))



@userPage.route('/')
def main():
    try:
        user = auth.getUserFromToken(g.token)
    except profile.UserNotFoundError:
        return "Error"
    return redirect(url_for("main.user.maind",id=user.id))

@userPage.route('/<int:id>')
def maind(id):
    return render_template("user/main.html", id=id)

def test():
    pass

