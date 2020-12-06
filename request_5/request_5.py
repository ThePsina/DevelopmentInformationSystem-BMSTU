from flask import render_template, Blueprint, current_app
from manager_ctx import UseDatabase

request_5 = Blueprint('request_5', __name__, template_folder='templates')


@request_5.route('/', methods=['GET'])
def req_5():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        drivers = find_drivers(cursor)
    return render_template('result_5.html', drivers=drivers)


def find_drivers(cursor):
    sql = f"SELECT id, driver_name, driver_surname, birth FROM Driver " \
          f" WHERE start_working=(SELECT min(start_working) FROM Driver) and end_working is not null;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'driver_name', 'driver_surname', 'birth']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
