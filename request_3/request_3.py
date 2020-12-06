from flask import render_template, Blueprint, current_app
from manager_ctx import UseDatabase

request_3 = Blueprint('request_3', __name__, template_folder='templates')


@request_3.route('/', methods=['GET'])
def req_3():
    with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
        drivers = find_drivers(cursor)
    return render_template('result_3.html', drivers=drivers)


def find_drivers(cursor):
    sql = f"SELECT driver_name FROM Driver d" \
          f" LEFT JOIN Schedule s on s.driver_id=d.id" \
          f" WHERE s.terminal_id IS NULL;" \

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['driver_name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
