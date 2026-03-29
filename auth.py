from functools import wraps
from flask import session, redirect, url_for, flash
from database import get_user_by_id


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('कृपया पहले लॉगिन करें', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('कृपया पहले लॉगिन करें', 'warning')
                return redirect(url_for('login'))
            user = get_user_by_id(session['user_id'])
            if not user or user['role'] != role:
                flash('आपको इस पेज की अनुमति नहीं है', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    if 'user_id' in session:
        return get_user_by_id(session['user_id'])
    return None
