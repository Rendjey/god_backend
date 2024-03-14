def login_nickname_mail_valid(login, nickname, mail, refer_nickname, conn):
    valid = {}
    valid['register_status'] = "success"
    cur = conn.cursor()

    sql = "SELECT * FROM reg_auth_card_db WHERE login = '" + login + "'"
    cur.execute(sql)
    count = cur.rowcount
    if count:
        valid['login_valid'] = "login is used"
        print(valid['login_valid'])
        valid['register_status'] = "failed"
    else:
        valid['login_valid'] = "success"

    sql = "SELECT * FROM reg_auth_card_db WHERE nickname = '" + nickname + "'"
    cur.execute(sql)
    count = cur.rowcount
    if count:
        valid['nickname_valid'] = "nickname is used"
        valid['register_status'] = "failed"
    else:
        valid['nickname_valid'] = "success"

    sql = "SELECT * FROM reg_auth_card_db WHERE mail = '" + mail + "'"
    cur.execute(sql)
    count = cur.rowcount
    if count:
        valid['mail_valid'] = "mail is used"
        valid['register_status'] = "failed"
    else:
        valid['mail_valid'] = "success"
    
    sql = "SELECT * FROM reg_auth_card_db WHERE nickname = '" + refer_nickname + "'"
    if refer_nickname != 'none':
        cur.execute(sql)
        count = cur.rowcount
        if count:
            valid['refer_valid'] = "success"
            print(valid['refer_valid'])
        else:
            valid['refer_valid'] = "referer not found"
            valid['register_status'] = "failed"

    return valid