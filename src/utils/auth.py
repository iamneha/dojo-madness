"""Authentication."""

from functools import wraps
from flask import session as api_session, request
from src.models.users import Users, UsersSchema
from src.utils.exceptions import HTTPError
from src.models.db import db_session as session


def authenticate_user(username, password):
    """Authenticate user."""
    users_schema = UsersSchema()
    result = session.query(Users)\
        .filter(Users.username == username).first()
    obj, err = users_schema.dump(result)
    if err:
        return {}
    if password != obj.get('password'):
        return {}
    return obj


def login_required(view):
    """Verify login credentials."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        token = request.headers.get('token') or api_session.get('token')
        users_schema = UsersSchema()
        username = password = None
        if auth:
            username = auth.username
            password = auth.password
            authenticate_user_resp = authenticate_user(username, password)
            if not authenticate_user_resp:
                raise HTTPError(401)
            api_session['token'] = authenticate_user_resp.get('user_secret')
        elif token:
            result = session.query(Users)\
                .filter(Users.user_secret == token).first()
            obj, err = users_schema.dump(result)
            if err:
                raise HTTPError(401, err)
            api_session['token'] = token
        else:
            raise HTTPError(401, "Unauthorized!")
        return view(*args, **kwargs)
    return wrapper
