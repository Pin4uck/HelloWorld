import sqlite3
import pb


def inquiry(s):
    try:
        conn = sqlite3.connect('currency.db')
    except Exception as e:
        return result
    curs = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS ccy (
                    id INTEGER NOT NULL PRIMARY KEY,
                    Abbreviation TEXT UNIQUE NOT NULL ,
                    Rate FLOAT NOT NULL,
                    last_updated timestamp default (strftime('%s', 'now')))''' 
                 )
    curs.execute(f'''SELECT Rate FROM ccy 
                        WHERE Abbreviation = '{s}' and (strftime('%s') - last_updated <= 20)''') 
    if row:
        return row[0][0]
    try:
        idd, abbr, ofcrate = pb.get_exchanges(s)
        curs.execute(f'''INSERT INTO ccy VALUES({idd}, '{abbr}', {ofcrate}, strftime("%s"))  
                                on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')
        conn.commit()
        if ofcrate:
            return ofcrate
    except Exception as e:
        print(e.__class__)
        curs.execute(f'''SELECT Rate FROM ccy 
                            WHERE Abbreviation = '{s}' ''')
        row = curs.fetchall()
        if row:
            return row[0][0]
    return = 'Ошибка приложения'
