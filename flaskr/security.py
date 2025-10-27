"""
Verwendet werkzeug.security.generate_password_hash und check_password_hash
(standardmäßig pbkdf2:sha256).
"""

from __future__ import annotations
from functools import wraps
from typing import Callable, List, Tuple
from flask import current_app, flash, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re


# -----------------------------
# Hashing & Verifikation
# -----------------------------

def hash_password(password: str) -> str:
    """Erzeugt sicheren Passwort-Hash mit werkzeug."""
    method = current_app.config.get("PASSWORD_METHOD", "pbkdf2:sha256")
    salt_length = int(current_app.config.get("PASSWORD_SALT_LENGTH", 16))
    return generate_password_hash(password, method=method, salt_length=salt_length)


def verify_password(password: str, password_hash: str) -> bool:
    """Prüft ein Klartextpasswort gegen gespeicherten Hash."""
    if not password_hash:
        return False
    return check_password_hash(password_hash, password)


def needs_rehash(password_hash: str) -> bool:
    """Prüft, ob der gespeicherte Hash aktualisiert werden sollte."""
    if not password_hash:
        return True
    configured = str(current_app.config.get("PASSWORD_METHOD", "pbkdf2:sha256"))
    return not str(password_hash).startswith(configured + "$") and not str(password_hash).startswith(configured + ":")


# -----------------------------
# Passwort-Policy
# -----------------------------

def check_password_policy(password: str) -> Tuple[bool, List[str]]:
    """Einfache Passwortregeln."""
    errors: List[str] = []
    min_len = int(current_app.config.get("PASSWORD_MIN_LENGTH", 8))
    if len(password) < min_len:
        errors.append(f"Passwort muss mindestens {min_len} Zeichen lang sein.")
    if not re.search(r"[a-z]", password):
        errors.append("Mindestens ein Kleinbuchstabe erforderlich.")
    if not re.search(r"[A-Z]", password):
        errors.append("Mindestens ein Großbuchstabe erforderlich.")
    if not re.search(r"\d", password):
        errors.append("Mindestens eine Zahl erforderlich.")
    if not re.search(r"[^\w\s]", password):
        errors.append("Mindestens ein Sonderzeichen erforderlich.")
    return (len(errors) == 0, errors)


# -----------------------------
# Login-Guard
# -----------------------------

def login_required(view: Callable) -> Callable:
    """Decorator für Routen, die Login erfordern."""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            if current_app.config.get("LOGIN_REQUIRED_FLASH", True):
                flash("Bitte zuerst einloggen.", "error")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view
