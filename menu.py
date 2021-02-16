import json
from flask import Flask, render_template, request, redirect, url_for, session
from request_1.request_1 import request_1
from request_2.request_2 import request_2
from request_3.request_3 import request_3
from request_4.request_4 import request_4
from request_5.request_5 import request_5
fr

from main_proccess.main_proccess import main_proc
from auth.auth import auth
from logout import delete_cookie

with open('data_files/dbconfig.json', 'r') as file_dbconfig:
    dbconfig = json.load(file_dbconfig)
with open('data_files/menu.json', 'r') as file_menu:
    menu_json = json.load(file_menu)
with open('data_files/query_access.json') as f:
    query_access_items = json.load(f)

app = Flask(__name__)
app.secret_key = "secret"
app.config['dbconfig'] = dbconfig
app.config['query_access'] = query_access_items


app.register_blueprint(request_1, url_prefix="/request_1")
app.register_blueprint(request_2, url_prefix="/request_2")
app.register_blueprint(request_3, url_prefix="/request_3")
app.register_blueprint(request_4, url_prefix="/request_4")
app.register_blueprint(request_5, url_prefix="/request_5")
app.register_blueprint(request_6, url_prefix="/request_6")
app.register_blueprint(proc, url_prefix='/proc')
app.register_blueprint(main_proc, url_prefix='/buss')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(delete_cookie, url_prefix='/delete-cookie')


@app.route('/menu/')
def menu():
    if 'user_group' not in session:
        session['user_group'] = 'Guest'

    route_mapping = {
        '1': url_for('auth.authorization'),
        '2': url_for('request_1.req_1'),
        '3': url_for('delete_cookie.del_cookie'),
        '5': url_for('request_2.req_2'),
        '6': url_for('request_3.req_3'),
        '7': url_for('request_4.req_4'),
        '8': url_for('request_5.req_5'),
        '9': url_for('request_6.req_6'),
        '10': url_for('proc.call'),
        '11': url_for('main_proc.call_main'),
    }
    point = request.args.get('point')

    if request.cookies.get("session") is None or session['user_group'] == 'Guest':
        return redirect(route_mapping['1'])
    if point is None:
        return render_template('menu.html', menu=menu_json, user_group=session['user_group'])
    elif point == '3':
        if 'cart' in session:
            session['cart'].clear()
        return redirect(route_mapping['3'])
    elif point in route_mapping:
        return redirect(route_mapping[point])
    else:
        return redirect(route_mapping['1'])


app.run(debug=True)
