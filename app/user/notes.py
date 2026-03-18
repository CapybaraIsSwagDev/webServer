# app/user.py
from flask import Blueprint, render_template, request, redirect, url_for, g
notesPage = Blueprint('notes', __name__, url_prefix="/notes")
from ..module import profile

# Check if user is Authenticated if not go to login screen
@notesPage.before_app_request
def admin_middleware():
    if not request.path.startswith("/notes"):
        return
    if not g.isAuthenticated:
        return redirect(url_for("main.auth.login"))

@notesPage.route('/')
def main():
    return "Hello"



