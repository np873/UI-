import sqlite3

class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

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
            'SELECT * FROM products WHERE categoryid LIKE ? ORDER BY name LIMIT ?', [categoryid, n])
        return [{
            'categoryid': d[0]
            ,'productid': d[1]
            ,'image': d[2]
            ,'name': d[3]
            ,'price': d[4]
            ,'weight': d[5]
            ,'discount': d[6]
        } for d in data]

    def get_product_detail(self, productid):
        print(productid)
        data = self.select(
            'SELECT * FROM products WHERE productid = ?', [productid])
        print(data)
        return [{
            'categoryid': d[0]
            ,'productid': d[1]
            ,'image': d[2]
            ,'name': d[3]
            ,'price': d[4]
            ,'weight': d[5]
            ,'discount': d[6]
        } for d in data]

    def get_cart_items(self, productid, quantity):
        data = self.select(
            'SELECT * FROM cart WHERE productid = ?', [productid])
        return [{
            'cartid': d[0],
            'productid': d[1],
            'name': d[2],
            'price': d[3],
            'weight': d[4],
            'quantity': d[5]
        } for d in data]

    def close(self):
        self.conn.close()