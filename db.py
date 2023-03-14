import sqlite3

class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    # query to return all columns for n bikes in database
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

 

    def close(self):
        self.conn.close()