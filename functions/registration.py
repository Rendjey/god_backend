from termcolor import colored
from flask import request
from functions.validation import login_nickname_mail_valid
import random
import datetime
import psycopg2

def registration(conn):
    data = request.form
    login = str(data['login'])
    nickname = str(data['nickname'])
    password = str(data['password'])
    mail = str(data['mail'])

    try:
        refer_nickname = str(data['refer_nickname'])
    except KeyError as e:
        refer_nickname = 'none'

    valid = login_nickname_mail_valid(login, nickname, mail, refer_nickname, conn)

    if valid['register_status'] != "success":
        return valid

    random_number = str(random.randint(1000, 2147483647))
    current_datetime = datetime.datetime.now()
    date_reg = current_datetime.strftime("%d-%m-%Y")
    cur = conn.cursor()
    sql = """INSERT INTO reg_auth_card_db (ID, login, nickname, password, refer_nickname, mail, date_reg)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    record_to_insert = (random_number, login, nickname, password, refer_nickname, mail, date_reg)
    cur.execute(sql, record_to_insert)
    conn.commit()
    sql = "SELECT * FROM reg_auth_card_db WHERE login = '" + login + "'"
    cur.execute(sql)
    count = cur.rowcount

    cur.execute("INSERT INTO dynamic_session_db (ID, balance, token, HdPz, kills, servtoken, CKS) VALUES (%s, '100', 'none', '0', '0', '001', '0.2')", [random_number])
    conn.commit()

    cur.close()
    conn.close()

    if count:
        register_status = "success"
    else:
        register_status = "failed"

    pdata = valid
    pdata['register_status'] = register_status

    message = colored(login, "light_grey") + " is register " + colored(register_status, "magenta") + "."
    print(message)

    return pdata