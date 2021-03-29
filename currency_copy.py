import sqlite3  # импорт библиотеки
def inquiry():  # создаем функцию
    conn = sqlite3.connect('currency.db')  # подключаемся к БД, если ее нет - создается
    curs = conn.cursor()  
    
    # создаем таблицу ссу если она не создана. далее добавляем необходимые столбцы с ограничениями.
    curs.execute('''CREATE TABLE IF NOT EXISTS ccy (  
                    id INTEGER NOT NULL PRIMARY KEY,
                    last_updated timestamp default (strftime('%s', 'now')),
                    Abbreviation TEXT UNIQUE NOT NULL ,
                    Rate FLOAT NOT NULL)'''  # в БД создаем таблицу с нужными столбцами и ограничениями
                 )


    a = input('''Введите интересующую вас валюту, например: 'USD', 'EUR', 'RUB' ''')  # ввод
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} and (strftime('%s') - last_updated <= 20)'''.format(a))  # запрос на вывод значения с таблицы, если значение есть или если оно не устарело                                                                                 # обновлялось более last_updated назад, значение не быдет выведено
    row = curs.fetchall()  # в этой переменной сохраняем значение запроса
    if row:  # если есть значение
        print('проверка(с базы)')
        return row[0][0]  # выводим и закрываем функцию
    curs.execute('''INSERT INTO ccy VALUES(1, strftime("%s"), "usd", 2.5)  
                    on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')  # вносим 3 строки значений, так же исключаем конфликт. Обновляем записи в строке если они устарели
    curs.execute('''INSERT INTO ccy VALUES(2, strftime("%s"), "eur", 3)
                    on conflict (id) do update set Rate=excluded.Rate, last_updated = excluded.last_updated''')
    curs.execute('''INSERT INTO ccy VALUES(3, strftime("%s"), "rub", 3.5)
                    on conflict(id) do update set Rate = excluded.Rate, last_updated = excluded.last_updated''')
    conn.commit()  # завершаем сессию, не уверен что нужно здесь
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(a))  # делаем запрос в таблицу БД
    row = curs.fetchall()  # сохраняем данные в переменной
    if row:  # если получили данные 
        print('проверка(обновленное значение)')
        return row[0][0]  # выводим и закрываем функцию
    curs.execute('''SELECT Rate FROM ccy 
                    WHERE Abbreviation = {} '''.format(a))  # делаем запрос в БД если не получили данные до сих пор, выводим даже устаревшее значение
    row = curs.fetchall()
    if row:  # если удалось получить данные с запроса
        print('проверка(необновленное значение)')
        return row[0][0]  # выводим
    result = 'Извините. Ошибка приложения'  
    return result  # если не удалось получить данные - сообщаем об ошибке


inquiry()
