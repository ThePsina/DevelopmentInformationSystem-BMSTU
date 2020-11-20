from functools import wraps
from flask import session, current_app, render_template


def check_query_access(point):
    def _check_query_access(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role_mapping = current_app.config['query_access']
            if session['user_group'] not in role_mapping[point]:
                return render_template('access_denied.html', needed=" или ".join(role_mapping[point]))
            else:
                return func(*args, **kwargs)
        return wrapper
    return _check_query_access
