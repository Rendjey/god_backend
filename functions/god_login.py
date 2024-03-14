from termcolor import colored
from flask import request
import re
from functions.token_generator import tokenize

def god_login(conn):
    data = request.form
    login = str(data['login'])
    password = str(data['password'])
    token = tokenize()
    
    sql = "SELECT * FROM reg_auth_card_db WHERE login = %s AND password = %s"
    record_to_insert = (login, password)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql, record_to_insert)
    count = cur.rowcount

    cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [login])
    id_fetch = cur.fetchone()
    id_str = re.sub("[^A-Za-z0-9]", "", str(id_fetch))
    
    cur.execute("UPDATE dynamic_session_db SET token = %s WHERE ID = %s", [str(token), str(id_str)])

    cur.close()
    conn.close()

    if count:
        login_status = "success"
    else:
        login_status = "failed"

    message = colored(login, "cyan") + " is login " + colored(login_status, "yellow") + "."
    print(message)


    pdata = {
        "login": login,
        "token": token,
        "login_status": login_status
    }

    return pdata