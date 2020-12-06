import json

from flask import render_template, request, Blueprint, current_app, session
from manager_ctx import UseDatabase

proc = Blueprint('proc', __name__, template_folder='templates')


with open('data_files/access.json', 'r') as f:
    access = json.load(f)


@proc.route('/', methods=['GET', 'POST'])
def call():
    if session['user_group'] not in access['groups']:
        return render_template('access_error.html')
    if 'send' in request.form and request.form['send'] == 'send':
        year = request.form['year']
        month = request.form['month']

        print(year, month)
        if year:
            with UseDatabase(current_app.config['dbconfig']["Manager"]) as cursor:
                drivers = find_drivers(cursor, year, month)
            return render_template('result_proc.html', drivers=drivers)
        else:
            return render_template('enter_proc.html')
    else:
        return render_template('enter_proc.html')


def find_drivers(cursor, year, month):
    args = (year, month,)
    cursor.execute(f"truncate table report;")
    result_procedure = cursor.callproc('sold_tickets_in_year', args)
    sql = f"select report_way, report_year, report_month, tickets_num from report;"

    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    schema = ['report_way', 'report_year', 'report_month', 'tickets_num']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res
