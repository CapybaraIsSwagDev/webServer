# app/modules/auth.py
import secrets, time, json, os
from pymemcache.client.base import Client
from . import profile

memcached_host = os.getenv('MEMCACHED_HOST', 'localhost')
mc = Client((memcached_host, 11211))

TOKENVALIDTIME = 3600 # in seconds 3600s = 1h

# Creates session
def createSession(User: profile.User) -> str:
    newtoken = secrets.token_hex(32)
    session_data = {
        "userId": User.id,
        "expires": time.time() + 3600
    }
    mc.set(newtoken, json.dumps(session_data), expire=TOKENVALIDTIME)
    return newtoken

def validToken(token: str) -> bool:
    if not token: return False
    
    raw_data = mc.get(token)
    if raw_data is None:
        return False

    
    reg = json.loads(raw_data)
    if reg["expires"] < time.time():
        removeToken(token)
        return False
    return True

def getUserFromToken(token:str) -> profile.User:
    if not token: raise profile.UserNotFoundError
    
    raw_data = mc.get(token)
    if not raw_data: raise profile.UserNotFoundError

    reg = json.loads(raw_data)
    return profile.userById(reg["userId"])

def removeToken(token:str):
    mc.delete(token)
        
