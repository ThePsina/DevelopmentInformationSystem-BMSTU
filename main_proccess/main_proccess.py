import json

from flask import render_template, request, Blueprint, current_app, session
from manager_ctx import UseDatabase

main_proc = Blueprint('main_proc', __name__, template_folder='templates')

with open('data_files/access.json', 'r') as f:
    access = json.load(f)


@main_proc.route('/', methods=['GET', 'POST'])
def call_main():
    if session['user_group'] not in access['groups']:
        return render_template('access_error.html')
    if 'send' in request.form and request.form['send'] == 'send':
        driver = request.form['driver']
        way = request.form['way']

        print(driver, way)
        with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
            post(cursor, driver, way)
    elif 'delete' in request.form and request.form['delete'] == 'delete':
        sch = request.form['id_s']

        print(sch)
        with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
            delete(cursor, sch)
    elif 'update' in request.form and request.form['update'] == 'update':
        driver = request.form['driver']
        way = request.form['way']
        sch = request.form['id_s']

        print(driver, way, sch)
        with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
            update(cursor, driver, way, sch)
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        schedule = get(cursor)
        drivers = get_drivers(cursor)
        ways = get_ways(cursor)
    return render_template('enter_main.html', schedule_get=schedule, drivers=drivers, ways=ways)


def get_drivers(cursor):
    sql = f"select driver_surname from Driver;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['driver_surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def get_ways(cursor):
    sql = f"select way_name from Way;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['way_name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def get(cursor):
    sql = f"select distinct s.id, driver_surname, way_name " \
          f"from Schedule s join Driver d on d.id=s.driver_id join Way w on w.id=s.way_id;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'driver_surname', 'way_name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def post(cursor, driver, way):
    sql = f"insert into Schedule (driver_id, way_id, terminal_id) " \
          f"values ((select id from Driver where driver_surname='{driver}'), " \
          f"(select id from Way where way_name='{way}'), 1);"
    cursor.execute(sql)


def delete(cursor, id_s):
    sql = f"delete from Schedule where id={id_s}"
    cursor.execute(sql)


def update(cursor, driver, way, id_s):
    sql = f"update Schedule " \
          f"set way_id=(select id from Way where way_name='{way}'), " \
          f"driver_id=(select id from Driver where driver_surname='{driver}') where id={id_s};"
    cursor.execute(sql)
