# Niki Patel, np873@drexel.edu
# CS530: DUI, Assignment [1]

import os

from flask import Flask, g, jsonify, render_template, request

from db import Database

DATABASE_PATH = 'categories.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    data = get_db().get_categories(12)
    return render_template('home.html', data = data)

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

@app.route('/categories')
def categories():
    data = get_db().get_categories(12)
    return render_template('categories.html', data = data) 

@app.route('/api/get_categories')
def api_get_categories():
    n = request.args.get('n', default=12)
    categories = get_db().get_categories(n)
    return jsonify(categories) 

@app.route('/products')
def products():
    categoryid = request.args.get('categoryid')
    print(categoryid)
    db = Database('products.db')
    data = db.get_products(categoryid, 12)
    return render_template('products.html', data=data)


@app.route('/api/get_products')
def api_get_products():
    db = Database('products.db')
    n = request.args.get('n')
    categoryid = request.args.get('categoryid')
    products = db.get_products(categoryid, n)
    return jsonify(products)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
