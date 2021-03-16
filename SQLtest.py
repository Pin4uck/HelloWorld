import sqlite3
import csv


db = sqlite3.connect('currency.db')
curs = db.cursor()
curs.execute('''create table ccy (Abbreviation text, Rate float)''')
db.commit()


int_str = 'INSERT INTO ccy values(?, ?)'
with open('currency.csv', 'rt') as infile:
    currency = csv.DictReader(infile)
    for ccy in currency:
        curs.execute(int_str, (ccy['Abbreviation'], ccy['Rate']))
    db.commit()


curs.execute('''SELECT Rate FROM ccy 
WHERE Abbreviation = {} '''.format(input()))
row = curs.fetchall()
print(row[0][0])
