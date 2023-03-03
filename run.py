# Niki Patel, np873@drexel.edu
# CS530: DUI, Assignment [1]

import os

from flask import Flask, g, json, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)