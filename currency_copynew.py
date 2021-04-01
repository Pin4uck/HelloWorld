import sqlite3
import pb_copy


def inquiry(s):

    conn = sqlite3.connect('currency.db')  # подключаемся к БД, если ее нет - создается
    curs = conn.cursor()  # предназ для рабботы с запросами
    curs.execute('''CREATE TABLE IF NOT EXISTS ccy (
                    id INTEGER NOT NULL PRIMARY KEY,
                    Abbreviation TEXT UNIQUE NOT NULL ,
                    Rate FLOAT NOT NULL,
                    last_updated timestamp default (strftime('%s', 'now')))'''  # в БД создаем таблицу с нужными столбцами и ограничениями
                 )



    curs.execute('''SELECT Rate FROM ccy 
            WHERE Abbreviation = {} and (strftime('%s') - last_updated <= 20)'''.format(s))  # запрос на вывод значения с таблицы, если значение в таблице                                                                                 # обновлялось более last_updated назад, значение не быдет выведено
    row = curs.fetchall()  # в этой переменной сохраняем значение запроса
    abbr, ofcrate, idd = pb_copy.get_exchange(s)
    if row:
        print('проверка(с базы)')
        return row

    curs.execute(f'''INSERT INTO ccy VALUES({idd}, {abbr}, {ofcrate}, strftime("%s"))  
                    on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')  # вносим 3 строки значений, так же исключаем ограничение и обновляем записи в строке если вышло время обновления

    conn.commit()
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(s))  # делаем запрос в таблицу БД
    row = curs.fetchall()  # сохраняем данные в переменной
    if row:  # если нет в таблице значения - делаем действия ниже:
        print('проверка(обновленное значение)')
        return row
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(s))
    row2 = curs.fetchall()
    if row2:
        print('проверка(необновленное значение)')
        return row2
    result = 'Извините. Ошибка приложения'
    return result


inquiry(input())
