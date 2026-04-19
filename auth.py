import os
import sqlite3
import hashlib

# db path
db = "users.db"

# set THe databse

def init_db():
    # create table if the user is just starting the app
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                password_hash BLOB NOT NULL
            )"""
        )

# hash the password, simpel stuff

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)


def clean_username(name):
    return (name or "").strip()

# check if the user exists in the database
def user_exists(username):
    username = clean_username(username)
    if not username:
        return False

    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    return row is not None


# create user in the database
def create_user(username, password):
    username = clean_username(username)
    if not username:
        raise ValueError("Username cannot be empty")

    if user_exists(username):
        raise ValueError("Username already exists")

    salt = os.urandom(16)
    password_hash = hash_password(password, salt)

    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
            (username, salt, password_hash),
        )

# authenticate the user by checking the password hash
def authenticate(username, password):
    username = clean_username(username)
    if not username:
        return False

    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT salt, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        return False

    salt, stored_hash = row
    return hash_password(password, salt) == stored_hash

# THought this would be cool so addinf change password function
def change_password(username, old_password, new_password):
    username = clean_username(username)
    if not username or not old_password or not new_password:
        return False
    if not authenticate(username, old_password):
        return False
    salt = os.urandom(16)
    new_hash = hash_password(new_password, salt)
    with sqlite3.connect(db) as conn:
        conn.execute(
            "UPDATE users SET salt = ?, password_hash = ? WHERE username = ?",
            (salt, new_hash, username),
        )
    return True 
# if the user is in a hurry and just wants to quickly test the app, they can use admin and admin.

def ensure_default_admin():
     init_db()

     # this is an easter egg. 
     admin_user = os.getenv("APP_ADMIN_USER", "admin")
     admin_pw = os.getenv("APP_ADMIN_PASSWORD", "admin")

     with sqlite3.connect(db) as conn:
        exists = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (admin_user,),
        ).fetchone()

     if not exists:
        try:
            create_user(admin_user, admin_pw)
        except sqlite3.IntegrityError:
            # If someone else created it first, that's fine.
            pass

