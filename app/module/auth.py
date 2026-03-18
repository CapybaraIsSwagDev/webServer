# app/modules/auth.py
import secrets, time
from werkzeug.security import generate_password_hash, check_password_hash
from . import profile
TOKENVALIDTIME = 3600 # in seconds 3600s = 1h

sessions = {}

# Creates session
def createSession(User: profile.User) -> str:
    newtoken = secrets.token_hex(32)
    sessions[newtoken] = {
        "userId": User.id,
        "expires": time.time() + 3600
    }
    return newtoken

def validToken(token: str) -> bool:
    reg = sessions.get(token)
    if reg == None:
        return False
    if reg["expires"] - time.time() > 3600:
        removeToken(token)
        return False 
    else:
        return True

def getUserFromToken(token:str) -> profile.User:
    if not token:
        raise profile.UserNotFoundError
    reg = sessions.get(token)

    return profile.userById(reg["userId"])

def removeToken(token:str):
    sessions.pop(token)
        
