from flask import request
import re

def balance(conn):
    data = request.form
    login = str(data['login'])
    
    cur = conn.cursor()
    
    cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [login])

    id_fetch = cur.fetchone()
    id_str = re.sub("[^A-Za-z0-9]", "", str(id_fetch))

    cur.execute("SELECT balance FROM dynamic_session_db WHERE ID = %s", [id_str])

    balance_fetch = cur.fetchone()
    balance_str = re.sub("[^A-Za-z0-9.]", "", str(balance_fetch))

    balance = {
        "balance": balance_str
    }

    return balance