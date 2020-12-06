from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_2 = Blueprint('request_2', __name__, template_folder='templates')


@request_2.route('/', methods=['GET', 'POST'])
def req_2():
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']

        print(year, month)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                drivers = find_drivers(cursor, year, month)
            return render_template('result_2.html', drivers=drivers)
        else:
            return render_template('enter_2.html')
    else:
        return render_template('enter_2.html')


def find_drivers(cursor, year, month):
    sql = f"SELECT d.id as id, d.driver_name as name, sum(hour(Time_arrived)-hour(Time_departure))*-1 as dif" \
          f" FROM Schedule s" \
          f" JOIN Driver d ON d.id = s.driver_id" \
          f" JOIN Terminal t ON t.id = s.terminal_id" \
          f" WHERE MONTH(Time_departure)='{month}'" \
          f" AND YEAR(Time_departure)='{year}'" \
          f" GROUP BY d.id;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'name', 'dif']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
