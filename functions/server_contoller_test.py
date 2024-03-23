from flask import request
import re
import math
import json
import os

def server_controller_test(conn):
    data = request.form
    token = str(data['token'])
    enterout = str(data['enterout'])

    cur = conn.cursor()
    
    cur.execute("SELECT ID, balance, HdPz FROM dynamic_session_db WHERE token = %s", [str(token)])
    id_fetch, balance, HdPz = cur.fetchone()
    try:
        f = open('hdpz.txt','r')
        hdpz = f.read()
        f.close()
        os.remove('hdpz.txt')
    except:
        hdpz = 0

    HdPz = round((float(HdPz) + float(hdpz)), 2)
    cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(HdPz), str(id_fetch)])
    cur.execute("SELECT login, nickname FROM reg_auth_card_db WHERE ID = %s", [str(id_fetch)])
    login, nickname = cur.fetchone()

    pdata = {}

    if(enterout == "enter"):
        cur.execute("INSERT INTO server_date_test (login, token) VALUES (%s, %s)", [str(login), str(token)])
        pdata = {
            "nickname": str(nickname),
            "balance": str(balance),
            "token": str(token),
            "hdpz": str(HdPz)
        }

    elif(enterout == "out"):
        cur.execute("UPDATE dynamic_session_db SET HdPz = '0' WHERE ID = %s", [str(id_fetch)])
        cur.execute("UPDATE dynamic_session_db SET kills = '0' WHERE ID = %s", [str(id_fetch)])
        cur.execute("UPDATE dynamic_session_db SET profit = '0' WHERE ID = %s", [str(id_fetch)])
        
        if(float(HdPz) != 0):
            HdPz_max = round(float((math.ceil((float(HdPz)/2)*100))/100), 2)
            HdPz_min = round(float((math.floor((float(HdPz)/2)*100))/100), 2)
            cur.execute("SELECT login FROM server_date_test")
            logins = cur.fetchall()
            
            if(int(len(logins)) == 1):
                cur.execute("DELETE FROM server_date_test WHERE login = %s", [str(login)])
                f = open('hdpz.txt','w')
                f.write(str(HdPz))
                f.close()
                pdata = {
                    "status": "ok"
                }
            
            else:
                cur.execute("DELETE FROM server_date_test WHERE login = %s", [str(login)])
                cur.execute("SELECT login FROM server_date_test")
                logins = cur.fetchall()

                if(int(len(logins)) == 1):
                    login_ed = str(re.sub("[^A-Za-z0-9]", "", str(logins)))
                    cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [str(login_ed)])
                    ed_id = str(re.sub("[^A-Za-z0-9]", "", str(cur.fetchone())))
                    cur.execute("SELECT HdPz FROM dynamic_session_db WHERE ID = %s", [ed_id])
                    ed_HdPz = round((float(str(re.sub("[^A-Za-z0-9.]", "", str(cur.fetchone())))) + float(HdPz)), 2)
                    cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(ed_HdPz), str(ed_id)])

                    pdata = {
                    "status": "success",
                    "first_login": login_ed,
                    "first_hdpz": str(ed_HdPz)
                    }

                    return pdata

                logins_for_sort = {}
                for login_el in logins:
                    login_el_srt = str(re.sub("[^A-Za-z0-9]", "", str(login_el)))
                    cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [login_el_srt])
                    id_el = str(re.sub("[^A-Za-z0-9]", "", str(cur.fetchone())))
                    cur.execute("SELECT HdPz FROM dynamic_session_db WHERE ID = %s", [id_el])
                    logins_for_sort[login_el_srt] = str(re.sub("[^A-Za-z0-9.]", "", str(cur.fetchone())))

                logins_sorted_rv = sorted(logins_for_sort.items(), key=lambda x: x[1], reverse=True)
                
                first_login = logins_sorted_rv[0]
                logins_sorted = sorted(logins_for_sort.items(), key=lambda x: x[1])
                last_login = logins_sorted[0]
                if (last_login == first_login):
                    last_login = logins_sorted[1]
                cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [str(first_login[0])])
                first_id = str(re.sub("[^A-Za-z0-9]", "", str(cur.fetchone())))
                cur.execute("SELECT HdPz FROM dynamic_session_db WHERE ID = %s", [first_id])
                first_HdPz = round((float(str(re.sub("[^A-Za-z0-9.]", "", str(cur.fetchone())))) + HdPz_max), 2)
                cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(first_HdPz), str(first_id)])
                cur.execute("SELECT ID FROM reg_auth_card_db WHERE login = %s", [last_login[0]])
                last_id = str(re.sub("[^A-Za-z0-9]", "", str(cur.fetchone())))
                cur.execute("SELECT HdPz FROM dynamic_session_db WHERE ID = %s", [str(last_id)])
                last_HdPz = round((float(str(re.sub("[^A-Za-z0-9.]", "", str(cur.fetchone())))) + HdPz_min), 2)  
                cur.execute("UPDATE dynamic_session_db SET HdPz = %s WHERE ID = %s", [str(last_HdPz), str(last_id)])

                pdata = {
                    "status": "success",
                    "first_login": first_login[0],
                    "first_hdpz": str(first_HdPz),
                    "last_login": last_login[0],
                    "last_hdpz": str(last_HdPz)
                }

        else:
            cur.execute("SELECT login FROM server_date_test")
            logins = cur.fetchall()
            cur.execute("DELETE FROM server_date_test WHERE login = %s", [str(login)])
            pdata = {
                "status": "success"
            }

    else:
        pdata = {
            "status": "CRITICAL_ERROR"
        }


    return pdata