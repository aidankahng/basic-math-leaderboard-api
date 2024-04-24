# For authentication
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from . import db
from .models import User
from datetime import datetime, timezone


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify(username, password):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar_one_or_none()
    if user is not None and user.check_password(password):
        return user
    return None


@basic_auth.error_handler
def handle_error(status_code):
    return {'error' : "Incorrect username and/or password. Please try again"}, status_code


@token_auth.verify_token
def verify(token):
    user = db.session.execute(db.select(User).where(User.token==token)).scalar_one_or_none()
    if user is not None and (user.token_expiration > datetime.now(timezone.utc)):
            return user
    return None


@token_auth.error_handler
def handle_error(status_code):
    return {'error' : "Incorrect token. Please try again"}, status_code