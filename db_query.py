import psycopg2
import re

conn = psycopg2.connect(dbname='test_db', user='tester', password='tester', host='localhost')
conn.autocommit = True
cur = conn.cursor()

cur.execute('SELECT * FROM server_date_test')

pr = cur.fetchall()
print(pr)

print("--------------")

cur.execute('SELECT ID, HdPz, kills, token FROM dynamic_session_db')
pr = cur.fetchall()
print(pr)

print("--------------")

cur.execute('SELECT ID, login FROM reg_auth_card_db')
pr = cur.fetchall()
print(pr)


cur.close()
conn.close()
