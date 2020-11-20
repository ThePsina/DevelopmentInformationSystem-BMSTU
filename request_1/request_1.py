from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_1 = Blueprint('request_1', __name__, template_folder='templates')


@request_1.route('/', methods=['GET', 'POST'])
def req_1():
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']
        way = request.form['way']

        print(year, month, way)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                drivers = find_drivers(cursor, year, month, way)
            return render_template('result.html', drivers=drivers)
        else:
            return render_template('enter_data.html')
    else:
        return render_template('enter_data.html')


def find_drivers(cursor, year, month, way):
    sql = f"select driver_name from Schedule " \
          f"join Driver on Schedule.driver_id = Driver.id " \
          f"join Terminal on Schedule.terminal_id = Terminal.id " \
          f"join Way on Schedule.way_id = Way.id " \
          f"where way_name = '{way}' " \
          f"and year(Time_arrived) = {year} " \
          f"and month(Time_arrived) = {month};"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['driver_name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
