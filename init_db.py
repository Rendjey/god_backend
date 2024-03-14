import os
import psycopg2

conn = psycopg2.connect(dbname='test_db', user='tester', password='tester', host='localhost')

cur = conn.cursor()

cur.execute('DROP TABLE reg_auth_card_db;')
cur.execute('DROP TABLE dynamic_session_db;')

cur.execute('CREATE TABLE reg_auth_card_db (ID serial PRIMARY KEY,'
                                 'login varchar (36) NOT NULL,'
                                 'nickname varchar (24) NOT NULL,'
                                 'password varchar (1024) NOT NULL,'
                                 'date_reg varchar (24) NOT NULL,'
                                 'refer_nickname varchar (24) NOT NULL,'
                                 'mail varchar (24) NOT NULL);'
                                 )

cur.execute('CREATE TABLE dynamic_session_db (ID serial PRIMARY KEY,'
                                 'balance varchar (24) NOT NULL,'
                                 'token varchar (24),'
                                 'HdPz varchar (50) NOT NULL,'
                                 'kills varchar (50) NOT NULL,'
                                 'servtoken varchar (50) NOT NULL,'
                                 'CKS varchar (50) NOT NULL);'
                                 )

sql = "INSERT INTO reg_auth_card_db (ID, login, nickname, password, date_reg, refer_nickname, mail) VALUES (0, 'medov', 'medov', 'c3d79edd62a17b3aefa05b2210eb10ac8507c11f850fa2583e0c94869f563421', '10-01-2024', 'admin', 'rendjey@mail.ru')"
cur.execute(sql)

sql = "INSERT INTO dynamic_session_db (ID, balance, token, HdPz, kills, servtoken, CKS) VALUES (0, '1000', '0', '0', '0', '0', '0.2')"
cur.execute(sql)


conn.commit()

cur.close()
conn.close()



