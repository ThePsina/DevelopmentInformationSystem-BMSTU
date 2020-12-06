from flask import render_template, request, Blueprint, current_app
from manager_ctx import UseDatabase

request_4 = Blueprint('request_4', __name__, template_folder='templates')


@request_4.route('/', methods=['GET', 'POST'])
def req_4():
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']

        print(year, month)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                drivers = find_drivers(cursor, year, month)
            return render_template('result_4.html', drivers=drivers)
        else:
            return render_template('enter_4.html')
    else:
        return render_template('enter_4.html')


def find_drivers(cursor, year, month):
    sql = f"select driver_surname from Driver d" \
          f" left join Schedule s on d.id = s.driver_id" \
          f" join Terminal t on s.terminal_id = t.id" \
          f" where month(Time_arrived) != {month} and year(Time_arrived) != {year}" \
          f" group by d.driver_surname;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['driver_surname']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
