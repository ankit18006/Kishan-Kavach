from functools import wraps
from flask import session, redirect, url_for, flash
from database import get_user_by_id
from models import get_translation


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            lang = session.get('language', 'en')
            flash(get_translation('please_login', lang), 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                lang = session.get('language', 'en')
                flash(get_translation('please_login', lang), 'warning')
                return redirect(url_for('login'))
            user = get_user_by_id(session['user_id'])
            if not user or user['role'] != role:
                lang = session.get('language', 'en')
                flash(get_translation('no_permission', lang), 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    if 'user_id' in session:
        return get_user_by_id(session['user_id'])
    return None


def get_user_language():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user:
            return user.get('language', 'en')
    return session.get('language', 'en')
