from flask import request
import re
from termcolor import colored

def kill_reg(conn):
    data = request.form
    killer = str(data['killer'])
    victim = str(data['victim'])
    
    cur = conn.cursor()
    
    #Killer block
    cur.execute("SELECT ID, login FROM reg_auth_card_db WHERE login = %s", [killer])
    conn.commit()

    id_fetch, login_fetch = cur.fetchone()
    id_killer = re.sub("[^A-Za-z0-9]", "", str(id_fetch))
    login_killer = re.sub("[^A-Za-z0-9]", "", str(login_fetch))

    #Killer balance
    cur.execute("SELECT balance, HdPz, kills FROM dynamic_session_db WHERE ID = %s", [id_killer])

    balance_fetch, HdPz_fetch, kills_fetch = cur.fetchone()
    balance_killer_str = re.sub("[^A-Za-z0-9.]", "", str(balance_fetch))
    HdPz_killer_fetch_str = re.sub("[^A-Za-z0-9.]", "", str(HdPz_fetch))
    kills_fetch_killer_fetch_str = re.sub("[^A-Za-z0-9]", "", str(kills_fetch))
    balance_killer = round((float(balance_killer_str) + 0.1), 2)
    HdPz_killer = round((float(HdPz_killer_fetch_str)), 2)
    kills_killer = int(kills_fetch_killer_fetch_str)
    cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])

    #Victim block
    cur.execute("SELECT ID, login FROM reg_auth_card_db WHERE login = %s", [victim])

    id_fetch, login_fetch = cur.fetchone()
    id_victim = re.sub("[^A-Za-z0-9]", "", str(id_fetch))
    login_victim = re.sub("[^A-Za-z0-9]", "", str(login_fetch))
    
    #Victim balance
    cur.execute("SELECT balance, HdPz FROM dynamic_session_db WHERE ID = %s", [id_victim])
    balance_fetch, HdPz_fetch = cur.fetchone()
    balance_victim_str = re.sub("[^A-Za-z0-9.]", "", str(balance_fetch))
    HdPz_victim_fetch_str = re.sub("[^A-Za-z0-9.]", "", str(HdPz_fetch))
    balance_victim = round((float(balance_victim_str) - 0.2), 2)
    HdPz_victim = round((float(HdPz_victim_fetch_str)), 2)
    cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_victim), str(id_victim)])
    HdPz_killer = round((float(HdPz_killer + HdPz_victim + float(0.05))), 2)
    
    if(kills_killer <= 8):
        kills_killer = kills_killer + 1
        cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(HdPz_killer), str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = %s WHERE ID = %s", [str(kills_killer), str(id_killer)])
    else:
        balance_killer = round((float(balance_killer + HdPz_killer)), 2)
        cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])
        HdPz_killer = 0
        kills_killer = 0
        cur.execute("UPDATE dynamic_session_db SET HdPz = '0' WHERE ID = %s", [str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = '0' WHERE ID = %s", [str(id_killer)])

    cur.execute("UPDATE dynamic_session_db SET HdPz = '0' WHERE ID = %s", [str(id_victim)])
    cur.execute("UPDATE dynamic_session_db SET kills = '0' WHERE ID = %s", [str(id_victim)])

    count = cur.rowcount
    cur.close()
    conn.close()

    if count:
        message = colored(login_killer, "light_green") + " kill " + colored(login_victim, "light_blue") + "."
        print(message)
    else:
        message = "Kill registered ERROR!"
        print(colored(message, "red"))

    pdata = {
        "login_killer": str(login_killer),
        "balance_killer": str(balance_killer),
        "hdpz_killer": str(HdPz_killer),
        "kills_killer": str(kills_killer),
        "login_victim": str(login_victim),
        "balance_victim": str(balance_victim),
    }

    return pdata