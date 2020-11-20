import json
from flask import Flask, render_template, request, redirect, url_for, session, make_response, Blueprint
from request_1.request_1 import request_1
from auth.auth import auth
from purchase.purchase import purchase
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
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(purchase, url_prefix='/purchase')
app.register_blueprint(delete_cookie, url_prefix='/delete-cookie')


@app.route('/menu/')
def menu():
    if 'user_group' not in session:
        session['user_group'] = 'Guest'

    route_mapping = {
        '1': url_for('auth.authorization'),
        '2': url_for('request_1.req_1'),
        '3': url_for('delete_cookie.del_cookie'),
        '72': url_for('purchase.purchase_func')
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
        return redirect(route_mapping['3'])


app.run(debug=True)
