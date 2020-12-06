from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_6 = Blueprint('request_6', __name__, template_folder='templates')


@request_6.route('/', methods=['GET', 'POST'])
def req_6():
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']
        way = request.form['way']

        print(year, month)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                drivers = find_drivers(cursor, year, month, way)
            return render_template('result_6.html', drivers=drivers)
        else:
            return render_template('enter_6.html')
    else:
        return render_template('enter_6.html')


def find_drivers(cursor, year, month, way):
    sql = f"select statistic_driver.driver_id, num from statistic_driver" \
          f" join Schedule on statistic_driver.driver_id=Schedule.driver_id" \
          f" join Terminal on Schedule.terminal_id = Terminal.id" \
          f" join Way on Schedule.way_id=Way.id" \
          f" where MONTH(Time_arrived) = {month}" \
          f" and YEAR(Time_arrived) = {year}" \
          f" and way_name = '{way}'"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['driver_id', 'num']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
