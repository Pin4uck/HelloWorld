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
                    last_updated timestamp default (strftime('%s', 'now')))'''  # в БД создаем таблицу с нужными столбцами и ограничениями
                 )
    curs.execute(f'''SELECT Rate FROM ccy 
                        WHERE Abbreviation = '{s}' and (strftime('%s') - last_updated <= 20)''')  # запрос на вывод значения с таблицы, если значение есть и оно не устаревшее                                                                                # обновлялось более last_updated назад, значение не быдет выведено
    row = curs.fetchall()  # в этой переменной сохраняем значение запроса
    if row:
        print('проверка(с базы)')
        return row[0][0]
    try:
        idd, abbr, ofcrate = pb.get_exchanges(s)
        curs.execute(f'''INSERT INTO ccy VALUES({idd}, '{abbr}', {ofcrate}, strftime("%s"))  
                                on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')
        conn.commit()
        curs.execute(f'''SELECT Rate FROM ccy 
                            WHERE Abbreviation = '{s}' and (strftime('%s') - last_updated <= 20)''')  # делаем запрос в таблицу БД
        row = curs.fetchall()
        if row:
            print('проверка(обновленное значение)')
            return row[0][0]
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
