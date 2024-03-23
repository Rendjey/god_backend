from flask import request
import re
from termcolor import colored

def kill_reg(conn):
    data = request.form
    killer = str(data['killer'])
    victim = str(data['victim'])
    
    cur = conn.cursor()

    ## Select Killer ID & login 
    cur.execute("SELECT ID, login FROM reg_auth_card_db WHERE login = %s", [killer])

    id_fetch, login_fetch = cur.fetchone()
    id_killer = re.sub("[^A-Za-z0-9]", "", str(id_fetch))
    login_killer = re.sub("[^A-Za-z0-9]", "", str(login_fetch))

    #Killer balance
    cur.execute("SELECT balance, HdPz, kills, profit FROM dynamic_session_db WHERE ID = %s", [id_killer])

    balance_fetch, HdPz_fetch, kills_fetch, profit_fetch = cur.fetchone()
    balance_killer_str = re.sub("[^A-Za-z0-9.]", "", str(balance_fetch))
    HdPz_killer_fetch_str = re.sub("[^A-Za-z0-9.]", "", str(HdPz_fetch))
    kills_fetch_killer_fetch_str = re.sub("[^A-Za-z0-9]", "", str(kills_fetch))
    
    profit_fetch_str = re.sub("[^A-Za-z0-9.]", "", str(profit_fetch))
    if(profit_fetch_str == "None"):
        profit_fetch_str = 0
    
    HdPz_killer = round((float(HdPz_killer_fetch_str)), 2)
    kills_killer = int(kills_fetch_killer_fetch_str)

    ## Select Victim ID & login
    cur.execute("SELECT ID, login FROM reg_auth_card_db WHERE login = %s", [victim])

    id_fetch, login_fetch = cur.fetchone()
    id_victim = re.sub("[^A-Za-z0-9]", "", str(id_fetch))
    login_victim = re.sub("[^A-Za-z0-9]", "", str(login_fetch))
    
    #Victim balance
    cur.execute("SELECT balance, HdPz, kills FROM dynamic_session_db WHERE ID = %s", [id_victim])
    balance_fetch, HdPz_fetch, kills_fetch_victim = cur.fetchone()
    balance_victim_str = re.sub("[^A-Za-z0-9.]", "", str(balance_fetch))
    HdPz_victim_fetch_str = re.sub("[^A-Za-z0-9.]", "", str(HdPz_fetch))
    kills_fetch_viktim_fetch_str = re.sub("[^A-Za-z0-9]", "", str(kills_fetch_victim))
    balance_victim = round((float(balance_victim_str) - 0.2), 2)
    HdPz_victim = round((float(HdPz_victim_fetch_str)), 2)
    cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_victim), str(id_victim)])


    if(str(kills_fetch_viktim_fetch_str) == "5"):
        balance_killer_str = float(balance_killer_str) + 0.01
        
        HdPz_killer = HdPz_killer - 0.01
    elif(str(kills_fetch_viktim_fetch_str) == "6"):
        balance_killer_str = float(balance_killer_str) + 0.02
        
        HdPz_killer = HdPz_killer - 0.02
    elif(str(kills_fetch_viktim_fetch_str) == "7"):
        balance_killer_str = float(balance_killer_str) + 0.03
        
        HdPz_killer = HdPz_killer - 0.03
    elif(str(kills_fetch_viktim_fetch_str) == "8"):
        balance_killer_str = float(balance_killer_str) + 0.04
        HdPz_killer = HdPz_killer - 0.04
    elif(str(kills_fetch_viktim_fetch_str) == "9"):
        balance_killer_str = float(balance_killer_str) + 0.05
        HdPz_killer = HdPz_killer - 0.05
    else:
        balance_killer_str = balance_killer_str
        ovpz_killer = 0

    HdPz_killer_012 = round((float(HdPz_killer + HdPz_victim + float(0.02))), 2)
    HdPz_killer_345 = round((float(HdPz_killer + HdPz_victim + float(0.03))), 2)
    HdPz_killer_678 = round((float(HdPz_killer + HdPz_victim + float(0.04))), 2)
    HdPz_killer_p = HdPz_killer
    

    if(kills_killer == 0 or kills_killer == 1 or kills_killer == 2):
        balance_killer = round((float(balance_killer_str) + 0.13), 2)
        cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])
        kills_killer = kills_killer + 1
        cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(HdPz_killer_012), str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = %s WHERE ID = %s", [str(kills_killer), str(id_killer)])
        HdPz_killer = HdPz_killer_012
        ##
    elif(kills_killer == 3 or kills_killer == 4 or kills_killer == 5):
        balance_killer = round((float(balance_killer_str) + 0.12), 2)
        cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])
        if(kills_killer == 4):
            ovpz_killer = 0.01
        if(kills_killer == 5):
            ovpz_killer = 0.02
        kills_killer = kills_killer + 1

        cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(HdPz_killer_345), str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = %s WHERE ID = %s", [str(kills_killer), str(id_killer)])
        HdPz_killer = HdPz_killer_345
        ##
    elif(kills_killer == 6 or kills_killer == 7 or kills_killer == 8):

        if(kills_killer == 6):
            ovpz_killer = 0.03
        if(kills_killer == 7):
            ovpz_killer = 0.04
        if(kills_killer == 8):
            ovpz_killer = 0.05
        balance_killer = round((float(balance_killer_str) + 0.11), 2)
        cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])
        kills_killer = kills_killer + 1
        cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(HdPz_killer_678), str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = %s WHERE ID = %s", [str(kills_killer), str(id_killer)])
        HdPz_killer = HdPz_killer_678
        ##
    elif(kills_killer == 9):

        HdPz_killer = round((float(HdPz_killer + HdPz_victim + float(0.04))), 2)
        balance_killer = round((float(balance_killer_str) + 0.11), 2)
        balance_killer = round((float(balance_killer + HdPz_killer)), 2)
        cur.execute("UPDATE dynamic_session_db SET balance = %s WHERE ID = %s", [str(balance_killer), str(id_killer)])
        HdPz_killer = 0
        kills_killer = 0
        cur.execute("UPDATE dynamic_session_db SET HdPz = '0' WHERE ID = %s", [str(id_killer)])
        cur.execute("UPDATE dynamic_session_db SET kills = '0' WHERE ID = %s", [str(id_killer)])
    
    cur.execute("UPDATE dynamic_session_db SET HdPz = '0' WHERE ID = %s", [str(id_victim)])
    cur.execute("UPDATE dynamic_session_db SET kills = '0' WHERE ID = %s", [str(id_victim)])
    
    profit_fetch_float = round((float(ovpz_killer) + float(HdPz_killer_p) + float(profit_fetch_str)), 2)
    
    cur.execute("UPDATE dynamic_session_db SET profit = %s WHERE ID = %s", [str(profit_fetch_float), str(id_killer)])
    
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
        "profit_killer" : str(profit_fetch_float),
        "ovpz_killer": str(ovpz_killer),
    }

    return pdata