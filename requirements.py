a = input('''Введите интересующую вас валюту, например: 'USD', 'EUR', 'RUB' ''')

# Делаем запрос в базу
curs.execute('''SELECT Rate FROM ccy
WHERE Abbreviation = {} '''.format(a))
row = curs.fetchall()


# Если в базе есть - выводим
if True:
    print(row[0][0])

# Иначе делаем запрос на сайт сохраняем в базе и выводим
# Запрос на сайт это файл pb.py
else:
    print(row[0][0])
