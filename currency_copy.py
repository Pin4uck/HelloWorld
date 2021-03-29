def inquiry():
    import sqlite3
    conn = sqlite3.connect('currency.db')  # подключаемся к БД, если ее нет - создается
    curs = conn.cursor()  # предназ для рабботы с запросами
    curs.execute('''CREATE TABLE IF NOT EXISTS ccy (
                    id INTEGER NOT NULL PRIMARY KEY,
                    last_updated timestamp default (strftime('%s', 'now')),
                    Abbreviation TEXT UNIQUE NOT NULL ,
                    Rate FLOAT NOT NULL)'''  # в БД создаем таблицу с нужными столбцами и ограничениями
                 )


    a = input('''Введите интересующую вас валюту, например: 'USD', 'EUR', 'RUB' ''')  # ввод
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} and (strftime('%s') - last_updated <= 20)'''.format(a))  # запрос на вывод значения с таблицы, если значение в таблице                                                                                 # обновлялось более last_updated назад, значение не быдет выведено
    row = curs.fetchall()  # в этой переменной сохраняем значение запроса
    if row:
        print('проверка(с базы)')
        return row[0][0]
    curs.execute('''INSERT INTO ccy VALUES(1, strftime("%s"), "usd", 2.5)  
                    on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')  # вносим 3 строки значений, так же исключаем ограничение и обновляем записи в строке если вышло время обновления
    curs.execute('''INSERT INTO ccy VALUES(2, strftime("%s"), "eur", 3)
                    on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')
    curs.execute('''INSERT INTO ccy VALUES(3, strftime("%s"), "rub", 3.5)
                    on conflict(id) do update set Rate = excluded.Rate, last_updated = excluded.last_updated''')
    conn.commit()  # завершаем сессию, не уверен что нужно здесь
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(a))  # делаем запрос в таблицу БД
    row = curs.fetchall()  # сохраняем данные в переменной
    if row:  # если нет в таблице значения - делаем действия ниже:
        print('проверка(обновленное значение)')
        return row[0][0]
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(a))
    row2 = curs.fetchall()
    if row2:
        print('проверка(необновленное значение)')
        return row2[0][0]
    result = 'Извините. Ошибка приложения'
    return result


inquiry()
