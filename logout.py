from flask import request, make_response, Blueprint, session, redirect

delete_cookie = Blueprint('delete_cookie', __name__)


@delete_cookie.route('/')
def del_cookie():
    if request.cookies.get("session") is None or session['user_group'] == 'Guest':
        return redirect('/menu')
    res = make_response("До свидания")
    res.set_cookie('session', request.cookies.get("session"), max_age=-1)
    return res
