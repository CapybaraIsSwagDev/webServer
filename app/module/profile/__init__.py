from werkzeug.security import generate_password_hash, check_password_hash
from .user import User
from ..database import get_db
import sqlite3

MIN_SIZE = 3
MAX_USERNAME = 15
MAX_PASSWORD = 20
MAX_EMAIL = 60


# -----------------------------
# User Errors Classes
# -----------------------------
class UserExistsError(Exception):
    """User with this username or email exists."""
    def __init__(self, message=None):
        if message is None:
            message = "User with this username or email exists."  # default message
        super().__init__(message)
    pass

class UserNotFoundError(Exception):
    """User was not found."""
    def __init__(self, message=None):
        if message is None:
            message = "User was not found."  # default message
        super().__init__(message)
    pass

class UserRegisterValueError(Exception):
    """The passed values were wrong"""
    def __init__(self, message=None):
        if message is None:
            message = "Passed values were wrong."  # default message
        super().__init__(message)
    pass


# -----------------------------
# User management functions
# -----------------------------
def registerUser(data:dict) -> User:
    required_fields = ["username", "email", "password"]
    if any(data.get(field, "") == "" for field in required_fields):
        raise UserRegisterValueError("One or more fields are empty.")
    try:
        newPassword = str(data.get("password","")[:MAX_PASSWORD]) # " " is a valid character
        newUsername = str(data.get("username","").strip()[:MAX_USERNAME]) # strip it so " abc" doesnt pass the len check
        newEmail    = str(data.get("email","").strip()) # We dont cut it because then it will be invalid
    except ValueError:
        raise UserRegisterValueError("Incorrect Values.")
    
    if (len(newPassword) < MIN_SIZE or len(newUsername) < MIN_SIZE or len(newEmail) < MIN_SIZE) or len(newEmail) > MAX_EMAIL :
        raise UserRegisterValueError("Too big or too small Values.")
    
    
    newHashed = generate_password_hash(newPassword)
    try:
        with get_db() as db:
            cursor = db.execute(
                "INSERT INTO users(username, email, password_hash) VALUES (?, ?, ?)",
                (newUsername, newEmail, newHashed)
            )
            user_id = cursor.lastrowid
        print(f"User {user_id} added successfully!")
        return userById(user_id)
    except sqlite3.IntegrityError:
        raise UserExistsError()


def userByUsername(username) -> User:
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
    if not row:
        raise UserNotFoundError()
    return User(row)


def userById(ID) -> User:
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE id = ?",
            (ID,)
        ).fetchone()
    if not row:
        raise UserNotFoundError()
    return User(row)

def searchUserByUsername(search_term: str) -> list[dict]:
    with get_db() as db:
        rows = db.execute(
        "SELECT id, username, xp FROM users WHERE username LIKE ? LIMIT 10",
        (f"{search_term}%",)
        ).fetchall()
    data = []
    for row in rows:
        data.append(User(row).getPublic(True))
    return data

def saveUser(user:User, full:bool = False):
    if user.id is None:
        raise ValueError("Cannot save user with no id")

    with get_db() as db:
        if full:
            query = """
            UPDATE users
            SET username = ?, email = ?, password_hash = ?, xp = ?
            WHERE id = ?
            """
            params = (user.username, user.hashed_password, user.xp, user.id)
        else:
            query = "UPDATE users SET xp = ? WHERE id = ?"
            params = (user.xp, user.id)

        cursor = db.execute(query, params)

        if cursor.rowcount == 0:
            raise ValueError("No user with that id")