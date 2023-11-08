import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='t',
                             password='123',
                             db='LearnTogether',
                             port=3331)

try:
    with connection.cursor() as cursor:
        sql = '''INSERT INTO `Group` (`Name`, `Description`) VALUES ("343ef23цук32s","e21e123")'''
        cursor.execute(sql)
        connection.commit()

    with connection.cursor() as cursor:

        sql = 'SELECT * FROM `Group`'
        cursor.execute(sql)

        # получение результатов запроса
        result = cursor.fetchall()
        print(result)
finally:
    # закрытие соединения с базой данных
    connection.close()
