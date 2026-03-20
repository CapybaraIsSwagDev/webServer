# app/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify
from ..module import auth, profile
import requests

api_auth = Blueprint('auth', __name__, url_prefix="/auth")

@api_auth.route('/sessions')
def debug():
    return auth.sessions

TURNSTILE_SECRET = "0x4AAAAAACWaR1PJzZdEay4J7g_4rK46u84"

def verify_captcha(data):
    return True
    token = data.get("cf-turnstile-response", "")
    if not token:
        return False

    resp = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET,
            "response": token,
            "remoteip": request.remote_addr
        }
    )

    result = resp.json()
    return result.get("success", False)


@api_auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # <- gets the JSON sent from fetch
        print(data)
        if not verify_captcha(data):
            return {"error":"Captha Failed"}
        required_fields = ["username", "password"]

        if any(data.get(field, "") == "" for field in required_fields): # Check all required fields so thay are not empty
            return {"error":"Empty fields"}

        try:
            activeUser = profile.userByUsername(data.get("username"))
            if not activeUser.checkPassword(data.get("password")):
                raise profile.UserNotFoundError()
        except profile.UserNotFoundError:
            return {"error":"Your password or Username is incorrect."}, 401

        token = auth.createSession(activeUser)
        dest = request.args.get("dest")

        if dest and dest.startswith("/"):
            resp = jsonify({"redirected":True,"url":"dest"})
        else:
            resp = jsonify({"redirected":True,"url":"/user"})
        resp.set_cookie("sessionToken", token, max_age=60*60, httponly=True, samesite="None", secure=True)  # cookie lasts 1 day
        return resp


@api_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() 
        if not verify_captcha(data):
            return {"error":"Captha Failed"} 
        required_fields = ["username", "email", "password"]

        if any(data.get(field, "") == "" for field in required_fields): # Check all required fields so thay are not empty
            return {"error":"Empty field"}
        try:
            profile.registerUser(data)
        except profile.UserExistsError:
            return {"error":"User with this Username or Email Already exists."}
        except profile.UserRegisterValueError:
            return {"error":"IDK"}

        return redirect(url_for("main.auth.login"))

    return render_template("auth/register.html")



@api_auth.route('/logout', methods=['POST'])
def logOut():
    print("Ask for logOut")
    auth.removeToken(request.cookies.get('sessionToken'))
    resp = jsonify({"message": "Logged out"})
    resp.set_cookie('sessionToken', '', expires=0)  # Clear cookie
    return resp
