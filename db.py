import sqlite3

class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def insert(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
        return c.lastrowid

    def get_categories(self, n):
        data = self.select(
            'SELECT * FROM categories ORDER BY categoryid ASC LIMIT ?', [n])
        return [{
            'categoryid': d[0]
            ,'image': d[1]
            ,'name': d[2]
        } for d in data]

    def get_products(self, categoryid, n):
        data = self.select(
            'SELECT * FROM products WHERE categoryid LIKE ? ORDER BY RANDOM() LIMIT ?', [categoryid, n])
        return [{
            'categoryid': d[0]
            ,'productid': d[1]
            ,'image': d[2]
            ,'name': d[3]
            ,'price': d[4]
            ,'weight': d[5]
            ,'discount': d[6]
            ,'discount_price': d[7]
        } for d in data] 

    def get_product_detail(self, productid):
        print(productid)
        data = self.select(
            'SELECT * FROM products WHERE productid = ?', [productid])
        return [{
            'categoryid': d[0]
            ,'productid': d[1]
            ,'image': d[2]
            ,'name': d[3]
            ,'price': d[4]
            ,'weight': d[5]
            ,'discount': d[6]
            ,'discount_price': d[7]
        } for d in data]

    def get_cart_items(self, userid, productid=None):
        if not productid:
            query = f"SELECT * FROM cart WHERE id = {userid}"
        else:
            query = f"SELECT * FROM cart WHERE id = {userid} and productid='{productid}'"
        data = self.select(query)
        return [{
            'cartid': d[0],
            'productid': d[1],
            'userid': d[2],
            'name': d[3],
            'price': d[4],
            'weight': d[5],
            'quantity': d[6],
            'image': d[7]
        } for d in data]

    def get_cart_items_count(self, userid):
        data = self.select(f'SELECT * FROM cart WHERE id = {userid}')
        return sum([d[6] for d in data])
    
    def get_top_deals(self):
        data = self.select(
            'SELECT * FROM products ORDER BY discount desc limit 12')
        return [{
            'categoryid': d[0]
            ,'productid': d[1]
            ,'image': d[2]
            ,'name': d[3]
            ,'price': d[4]
            ,'weight': d[5]
            ,'discount': d[6]
            ,'discount_price': d[7]
            } for d in data] 

    def remove_from_cart(self, productid, userid):
        print(f"Removing product {productid} from cart...")
        rows_deleted = self.conn.execute(
            "DELETE FROM cart WHERE productid = ? AND id = ?", (productid,userid)
        ).rowcount
        self.conn.commit()

    def clear_user_cart(self, userid):
        self.conn.execute(
            f"DELETE FROM cart WHERE id = {userid}"
        )
        self.conn.commit()

    def create_account(self, firstname, lastname, email, password):
        self.execute('INSERT INTO users (firstname, lastname, email, password) VALUES (?, ?, ?, ?)',
                     [firstname, lastname, email, password])


    def get_user(self, email):
        data = self.select(
            'SELECT * FROM users WHERE email=?', [email])
        if data:
            d = data[0]
            return {
                'userid': d[0],
                'firstname': d[1],
                'lastname': d[2],
                'email': d[3],
                'password': d[4],
            }
        else:
            return None

    def close(self):
        self.conn.close()