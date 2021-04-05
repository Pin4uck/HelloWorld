import sqlite3
import pb


def inquiry(s):
    try:
        conn = sqlite3.connect('E:\\currency.db')
    except Exception as e:
        print(e.__class__)
        result = 'Нет связи с БД'
        return result
    curs = conn.cursor()  # предназ для рабботы с запросами
    conn.execute('''CREATE TABLE IF NOT EXISTS ccy (
                    id INTEGER NOT NULL PRIMARY KEY,
                    Abbreviation TEXT UNIQUE NOT NULL ,
                    Rate FLOAT NOT NULL,
                    last_updated timestamp default (strftime('%s', 'now')))''' 
                 )
    curs.execute(f'''SELECT Rate FROM ccy 
                        WHERE Abbreviation = '{s}' and (strftime('%s') - last_updated <= 20)''') 
    if row:
        print('проверка(с базы)')
        return row[0][0]
    try:
        idd, abbr, ofcrate = pb.get_exchanges(s)
        curs.execute(f'''INSERT INTO ccy VALUES({idd}, '{abbr}', {ofcrate}, strftime("%s"))  
                                on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')
        conn.commit()
        if ofcrate:
            print('проверка(обновленное значение)')
            return ofcrate
    except Exception as e:
        print(e.__class__)
        curs.execute(f'''SELECT Rate FROM ccy 
                            WHERE Abbreviation = '{s}' ''')
        row = curs.fetchall()
        if row:
            print('проверка(необновленное значение)')
            return row[0][0]
    result = 'Ошибка приложения'
    return result


inquiry(input())
