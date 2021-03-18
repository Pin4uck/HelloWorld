import sqlite3


conn = sqlite3.connect('database.db')
curs = conn.cursor()


curs.execute('''CREATE TABLE IF NOT EXISTS ccy (
                id INTEGER NOT NULL PRIMARY KEY,
                Abbreviation TEXT UNIQUE NOT NULL ,
                Rate FLOAT NOT NULL)'''
             )


a = input('''Введите интересующую вас валюту, например: 'USD', 'EUR', 'RUB' ''')
curs.execute('''SELECT Rate FROM ccy 
WHERE Abbreviation = {} '''.format(a))
row = curs.fetchall()
if not row:
    curs.execute('INSERT INTO ccy VALUES(1, "usd", 2.5)')
    curs.execute('INSERT INTO ccy VALUES(2, "eur", 3)')
    curs.execute('INSERT INTO ccy VALUES(3, "rub", 3.5)')
    conn.commit()
    curs.execute('''SELECT Rate FROM ccy 
    WHERE Abbreviation = {} '''.format(a))
    row = curs.fetchall()
    print(row[0][0])
else:
    print(row[0][0])
