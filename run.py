from flask import Flask, g, jsonify, render_template, request,session, redirect
from db import Database
from passlib.hash import pbkdf2_sha256

DATABASE_PATH = 'mariocart.db'

app = Flask(__name__)
app.secret_key = b'demokeynotreal!'

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
    deals = get_db().get_top_deals()
    categories = get_db().get_categories(12)
    return render_template('home.html', categories=categories, deals=deals)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = get_db().get_user(email)
            if user:
                if pbkdf2_sha256.verify(password, user['password']):
                    session['user'] = user 
                    session['cart_quantity'] = get_db().get_cart_items_count(session['user']['userid'])               
                    return redirect('/')
            else:
                message = "User unknown, please try again"
        elif email and not password:
            message = "Missing password, please try again"
        elif not email and password:
            message = "Missing username, please try again"
    return render_template('sign_in.html', message=message)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        print('creating account: {}, {}, {}, {}'.format(firstname, lastname, email, password))
        if firstname and lastname and email and password:
            encrypted_password = pbkdf2_sha256.hash(password)
            get_db().create_account(firstname, lastname, email, encrypted_password)
            return redirect('/sign_in')
    return render_template('create_account.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        typed_password = request.form.get('password')
        if fname and lname and email and typed_password:
            encrypted_password = pbkdf2_sha256.hash(typed_password)
            get_db().create_user(fname, lname, email, encrypted_password)
            return redirect('/login')
        else :
            message = "Please enter all fields"
    return render_template('create_user.html', message=message)

@app.route('/logout')
def logout():
    session['cart_quantity'] = 0
    session.pop('user', None)
    return redirect('/')

# my_account function
@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

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
    data = get_db().get_products(categoryid, 12)
    category = get_db().get_categories(12)
    return render_template('products.html', data=data, category=category) 

@app.route('/api/get_products')
def api_get_products():
    n = request.args.get('n')
    categoryid = request.args.get('categoryid')
    products = get_db().get_products(categoryid, n)
    return jsonify(products)

@app.route('/api/get_product_detail')
def api_get_product_detail():
    productid = request.args.get('productid')
    product = get_db().get_product_detail(productid)
    return jsonify(product)

@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    userid = session['user'].get('userid')
    productid = data.get('productid')
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')
    weight = data.get('weight')
    image = data.get('image')
    session['cart_quantity'] = data.get('cartQuantity')
    # Create a new CartItem object
    productid = data.get('productid')
    quantity = data.get('quantity')
    existing_item = get_db().get_cart_items(userid, productid)
    if len(existing_item) == 0: 
        data = get_db().insert('INSERT INTO cart (productid, id, name, price, quantity, weight, image) VALUES (?, ?, ?, ?, ?, ?, ?)', (productid, userid, name, price, quantity, weight, image))
    else:
        get_db().insert('UPDATE cart SET quantity = quantity + ? WHERE id = ? AND productid = ?', (quantity, userid, productid))
    return jsonify({'status': 'success', 'message': 'Product added to cart successfully.'})

@app.route('/api/get_cart_items')
def api_get_cart_items():
    userid = session['user'].get('userid')
    cart_items = get_db().get_cart_items(userid)
    return jsonify(cart_items)

@app.route('/cart', strict_slashes=False)
def cart():
    userid = session['user'].get('userid')
    data = get_db().get_cart_items(userid)
    return render_template('cart.html', data=data)

@app.route('/api/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    userid = session['user'].get('userid')
    productid = data.get('productId')
    # Remove item from the cart
    get_db().remove_from_cart(productid, userid)
    session['cart_quantity'] = get_db().get_cart_items_count(userid)               

    return jsonify({'message': 'Product removed from cart successfully.'})

@app.route('/api/place_order', methods=['GET'])
def place_order():
    userid = session['user'].get('userid')
    get_db().clear_user_cart(userid)
    session['cart_quantity'] = 0
    return jsonify({'message': 'Order placed successfully'})

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
