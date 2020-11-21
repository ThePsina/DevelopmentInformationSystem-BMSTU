from flask import render_template, request, Blueprint, current_app, session
from manager_ctx import UseDatabase
import json

purchase = Blueprint('purchase', __name__, template_folder='templates')

with open('data_files/access.json', 'r') as f:
    access = json.load(f)


@purchase.route('/', methods=['POST', 'GET'])
def purchase_func():
    if session['user_group'] not in access['groups']:
        return render_template('error.html', text=f"Не хватает прав для этого действия")

    init_cart()
    with UseDatabase(current_app.config['dbconfig']['Manager']) as cursor:
        catalog = show_catalog(cursor)

        if 'choice' in request.form and request.form['choice'] == "Выбрать":
            choice_name = request.form.get('choice_name')
            choice_id = request.form.get('choice_id')
            amount = request.form.get('quantity')

            put_into_basket(choice_id, choice_name, amount)
            return render_template('catalog.html', catalog=catalog)

        elif 'show_basket' in request.form and request.form['show_basket'] == "Показать корзину":
            return render_template('cart.html', basket=session['cart'])

        elif 'exit' in request.form and request.form['exit'] == "Оформить заказ":
            save_basket(cursor)
            return render_template('catalog.html', catalog=catalog)

        elif 'delete' in request.form and request.form['delete'] == "Удалить":
            choice_name_delete = request.form.get('choice_name_delete')
            delete_from_basket(choice_name_delete)
            return render_template('cart.html', basket=session['cart'])

        else:
            return render_template('catalog.html', catalog=catalog)


def show_catalog(cursor):
    cursor.execute(f"SELECT id_catalog, name, amount, price FROM catalog")
    result = cursor.fetchall()
    res = []
    schema = ['id_catalog', 'name', 'amount', 'price']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def put_into_basket(choice_id, choice_name, amount):
    if 'cart' not in session:
        session['cart'] = []

    full_amount = 0
    for value in session['cart']:
        if int(choice_id) == value['choice_id']:
            full_amount = value['amount']
            session['cart'].remove(value)
            full_amount += int(amount)

    print(full_amount)
    if full_amount == 0:
        session['cart'] += [{
            'choice_id': int(choice_id),
            'choice_name': choice_name,
            'amount': int(amount)
        }]
    else:
        session['cart'] += [{
            'choice_id': int(choice_id),
            'choice_name': choice_name,
            'amount': int(full_amount)
        }]


def init_cart():
    if 'cart' not in session:
        session['cart'] = []


def save_basket(cursor):
    for i in range(len(session['cart'])):
        values = session['cart'][i].values()
        values = list(values)
        cursor.execute(f"INSERT INTO basket VALUES (NULL, %s, %s, %s)", (values[1], values[2], values[0],))

    if 'cart' in session:
        session['cart'] = []


def delete_from_basket(name):
    for value in session['cart']:
        if value['choice_name'] == name:
            session['cart'].remove(value)
    return
