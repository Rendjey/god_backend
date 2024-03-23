import re
import random
import psycopg2
from termcolor import colored
from functions.god_login import god_login
from functions.logging import main
from flask import Flask, render_template, request
from functions.registration import registration
from functions.kill_reg import kill_reg
from functions.balance import balance
from functions.server_contoller_test import server_controller_test


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

if __name__ == '__main__':
	app.run(host='0.0.0.0')

def get_db_connection():
    conn = psycopg2.connect(dbname='test_db', user='tester', password='tester', host='localhost')
    conn.autocommit = True
    return conn

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/version/", methods=['POST'])
def version():
    version_actual = '0.1'
    data = request.form
    version_client = str(data['version'])
    if(version_client == version_actual):
        verdict = {
            "version": "success"
        }
    else:
        verdict = {
            "version": "failed" 
        }
    return verdict

@app.route("/reg/", methods=['POST'])
def reg():
    conn = get_db_connection()
    pdata = registration(conn)
    
    return pdata

@app.route("/login/", methods=['POST'])
def login():
    conn = get_db_connection()
    pdata = god_login(conn)

    return pdata

@app.route("/kill/", methods=['POST'])
def kill_request():
    conn = get_db_connection()
    pdata = kill_reg(conn)

    return pdata

@app.route("/balance/", methods=['POST'])
def balance_request():
    conn = get_db_connection()

    return balance(conn)

@app.route("/test_server_controler/", methods=['POST'])
def test_server_controler():
    conn = get_db_connection()    
    pr = server_controller_test(conn)

    return pr


#
#   person013
#   cieOYBFLEjTCA5hySGfZv2z3
#
#   person014
#   nPbBa6cUjGyrOZ2KRNlA8JLw
#