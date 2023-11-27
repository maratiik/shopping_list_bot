from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import pathlib
from datetime import datetime
from db import db, Item

APP_PATH = pathlib.Path('shopping list bot').resolve()
DB_PATH = pathlib.Path('shopping list bot/shopping list.db').resolve()

# global authorized
# authorized = False

app = Flask(__name__, instance_path=APP_PATH)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'shopping_list.db')

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/purchase-history')
def purchase_history():
    return render_template('purchase_history.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/products')
def products():
    items = Item.query.order_by(Item.date.desc()).all()
    return render_template('products.html', items=items)


if __name__ == '__main__':
    if not DB_PATH.exists():
        with app.app_context():
            db.create_all()
    app.run(debug=True)