from flask import Blueprint, redirect, render_template, session, request, current_app
from manager_ctx import UseDatabase

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def authorization():
    if 'send' in request.form and request.form['send'] == 'auth':
        result = []

        login = request.form.get('login')
        password = request.form.get('password')

        if login and password:
            with UseDatabase(current_app.config['dbconfig']['Manager']) as cursor:
                cursor.execute(
                    f"SELECT role FROM user_groups WHERE login='%s' "
                    f"AND password='%s'" % (login, password)
                )

                schema = ['user_group']
                for con in cursor.fetchall():
                    result.append(dict(zip(schema, con)))

            if len(result) > 0:
                session['user_group'] = result[0]['user_group']
                return redirect('/menu')
            else:
                return render_template('auth.html')
    else:
        return render_template('auth.html')
