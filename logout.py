from flask import request, make_response, Blueprint, session

delete_cookie = Blueprint('delete_cookie', __name__)


@delete_cookie.route('/')
def del_cookie():
    res = make_response("До свидания")
    res.set_cookie('session', request.cookies.get("session"), max_age=-1)
    return res
