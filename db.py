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
            'SELECT * FROM categories ORDER BY id ASC LIMIT ?', [n])
        return [{
            'id': d[0]
            ,'image': d[1]
            ,'name': d[2]
        } for d in data]

    def close(self):
        self.conn.close()