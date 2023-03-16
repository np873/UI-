# Niki Patel, np873@drexel.edu
# CS530: DUI, Assignment [1]

import os

from flask import Flask, g, jsonify, render_template, request

from db import Database

import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate('/Users/nikipatel/Desktop/Niki/Winter22-23/UI/Project/serviceAccountKey/serviceKey.json')
firebase_admin.initialize_app(cred)

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
    return render_template('home.html', data=data)

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
    db = Database('products.db')
    data = db.get_products(categoryid, 12)
    category = get_db().get_categories(12)
    return render_template('products.html', data=data, category=category)


@app.route('/api/get_products')
def api_get_products():
    db = Database('products.db')
    n = request.args.get('n')
    categoryid = request.args.get('categoryid')
    products = db.get_products(categoryid, n)
    return jsonify(products)

@app.route('/api/get_product_detail')
def api_get_product_detail():
    db = Database('products.db')
    productid = request.args.get('productid')
    product = db.get_product_detail(productid)
    return jsonify(product)


@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cartid = data.get('cartid')
    productid = data.get('productid')
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')
    weight = data.get('weight')
    image = data.get('image')

    # Create a new CartItem object
    db = Database('cart.db')
    productid = data.get('productid')
    quantity = data.get('quantity')
    existing_item = db.get_cart_items(productid, quantity)
    if len(existing_item) == 0: 
        data = db.insert('INSERT INTO cart (cartid, productid, name, price, quantity, weight, image) VALUES (?, ?, ?, ?, ?, ?, ?)', (cartid, productid, name, price, quantity, weight, image))
        print(data)
    else:
        db.insert('UPDATE cart SET quantity = quantity + ? WHERE productid = ?', (quantity, productid))

    return jsonify({'message': 'Product added to cart successfully.'})


@app.route('/api/get_cart_items')
def get_cart_items():
    db = Database('cart.db')
    productid = request.args.get('productid')
    quantity = request.args.get('quantity')
    data = db.select('SELECT * FROM cart')
    cart = db.get_cart_items(productid, quantity)
    return jsonify(data)

@app.route('/cart')
def cart():
    db = Database('cart.db')
    data = db.select('SELECT * FROM cart')
    print(data)
    return render_template('cart.html', data=data)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
