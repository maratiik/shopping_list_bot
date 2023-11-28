from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import pathlib
from datetime import datetime
from db import db, Item, Log, History

APP_PATH = pathlib.Path('shopping list bot').resolve()
ITEMS_PATH = pathlib.Path('shopping list bot/shopping list.db').resolve()
LOG_PATH = pathlib.Path('shopping list bot/log.db').resolve()
HISTORY_PATH = pathlib.Path('shopping list bot/history.db').resolve()

# global authorized
# authorized = False

app = Flask(__name__, instance_path=APP_PATH)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'shopping_list.db')
# app.config['SQLALCHEMY_BINDS'] = {
#     'log': 'sqlite:///' + os.path.join(app.instance_path, 'log.db'),
#     'history': 'sqlite:///' + os.path.join(app.instance_path, 'history.db'),
# }

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logs')
def logs():
    log = Log.query.order_by(Log.date).all()
    return render_template('logs.html', log=log)


@app.route('/purchase-history')
def purchase_history():
    items = History.query.all()
    return render_template('purchase_history.html', items=items)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/products')
def products():
    items = Item.query.order_by(Item.date.desc()).all()
    return render_template('products.html', items=items)


@app.route('/add-product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        priority = int(request.form['priority']) % 4

        item = Item(name=name, url=url, priority=priority)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/products')
        except:
            return 'An error occured'
    else:
        return render_template('products_add.html')


@app.route('/products/<int:id>')
def detailed_product(id):
    item = Item.query.get(id)
    return render_template("products_detail.html", item=item)


@app.route('/products/<int:id>/delete')
def delete_product(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/products')
    except:
        return "An error occured!"


@app.route('/products/<int:id>/edit', methods=['POST', 'GET'])
def edit_product(id):
    item = Item.query.get(id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.url = request.form['url']
        item.priority = int(request.form['priority']) % 4

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return 'An error occured!'
    else:
        return render_template('products_edit.html', item=item)


if __name__ == '__main__':
    if not ITEMS_PATH.exists():
        with app.app_context():
            db.create_all()
    app.run(debug=True)
