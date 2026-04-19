import os
import sqlite3
import hashlib


# ============================================================================
#  Database setup
# ============================================================================

def _db_path() -> str:
    """
    Figure out where the DB lives.
    If AUTH_DB_PATH is set, use that. Otherwise drop a users.db next to this file.
    """
    override = os.getenv("AUTH_DB_PATH")
    if override:
        return override

    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "users.db")


def init_db() -> None:
    """Create the users table if it doesn't already exist."""
    with sqlite3.connect(_db_path()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                password_hash BLOB NOT NULL
            )
            """
        )


# ============================================================================
#  Internal helpers (these grew over time)
# ============================================================================

def _hash_password(password: str, salt: bytes) -> bytes:
    """
    Hash a password using PBKDF2.
    Nothing fancy — just a solid default.
    """
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120_000,
    )


def _norm_username(name: str) -> str:
    """
    Clean up the username a bit.
    Mostly here to avoid weird whitespace bugs.
    """
    return (name or "").strip()


# ============================================================================
#  User lookup + creation
# ============================================================================

def user_exists(username: str) -> bool:
    """Check if a username is already in the DB."""
    username = _norm_username(username)
    if not username:
        return False

    with sqlite3.connect(_db_path()) as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    return row is not None


def create_user(username: str, password: str) -> None:
    """
    Create a new user.
    Raises ValueError if username/password are missing.
    """
    username = _norm_username(username)
    if not username or not password:
        raise ValueError("Username and password required")

    salt = os.urandom(16)
    pw_hash = _hash_password(password, salt)

    with sqlite3.connect(_db_path()) as conn:
        conn.execute(
            "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
            (username, salt, pw_hash),
        )


# ============================================================================
#  Authentication + password changes
# ============================================================================

def authenticate(username: str, password: str) -> bool:
    """
    Return True if the username/password pair is valid.
    """
    username = _norm_username(username)
    if not username or not password:
        return False

    with sqlite3.connect(_db_path()) as conn:
        row = conn.execute(
            "SELECT salt, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row:
        return False

    salt, stored_hash = row
    return _hash_password(password, salt) == stored_hash


def change_password(username: str, old_password: str, new_password: str) -> bool:
    """
    Change a user's password.
    Returns True on success, False otherwise.
    """
    username = _norm_username(username)
    if not username or not old_password or not new_password:
        return False

    if not authenticate(username, old_password):
        return False

    new_salt = os.urandom(16)
    new_hash = _hash_password(new_password, new_salt)

    with sqlite3.connect(_db_path()) as conn:
        conn.execute(
            "UPDATE users SET salt = ?, password_hash = ? WHERE username = ?",
            (new_salt, new_hash, username),
        )

    return True


# ============================================================================
#  Default admin bootstrap
# ============================================================================

def ensure_default_admin() -> None:
    """
    Make sure there's at least one admin user.
    Uses APP_ADMIN_USER / APP_ADMIN_PASSWORD if set.
    """
    init_db()

    admin_user = os.getenv("APP_ADMIN_USER", "admin")
    admin_pw = os.getenv("APP_ADMIN_PASSWORD", "admin")

    with sqlite3.connect(_db_path()) as conn:
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
