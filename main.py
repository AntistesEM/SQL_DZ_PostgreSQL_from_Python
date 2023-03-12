import psycopg2


def insert_bd():
    cursor.execute("""
    INSERT INTO clients("name", surname) VALUES
        ('Adam', 'Smit'),
        ('Chris', 'Powers'),
        ('Susan', 'Brewer'),
        ('Toni', 'Matthews'),
        ('Sandra', 'Patterson');
    """)
    cursor.execute("""
    INSERT INTO phones(phone_number, client_id) VALUES
        ('+79998140555', 1),
        ('+79038140555', 1),
        ('+79638140555', 1),
        ('+79998140500', 2),
        ('+79998140501', 2),
        ('', 3),
        ('+79998140111', 4),
        ('+79998140001', 5),
        ('+79998140002', 5),
        ('+79998140003', 5),
        ('+79998140004', 5);
    """)
    cursor.execute("""
    INSERT INTO emails(email_name, client_id) VALUES
        ('adam@mail.com', 1),
        ('chris@mail.com', 2),
        ('susan@mail.com', 3),
        ('susan@yandex.com', 3),
        ('toni@mail.com', 4),
        ('sandra@mail.com', 5);
    """)


# Функции из ДЗ
# Функция, создающая структуру БД (таблицы)
def create_bd():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clients(
        Client_id SERIAL PRIMARY KEY,
        Name VARCHAR(20) NOT NULL,
        Surname VARCHAR(30) NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Phones(
        Phone_id SERIAL PRIMARY KEY,
        Phone_number VARCHAR(15) UNIQUE,
        Client_id INTEGER NOT NULL REFERENCES Clients(Client_id)
        );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Emails(
        Email_id SERIAL PRIMARY KEY,
        Email_name VARCHAR(60) NOT NULL UNIQUE,
        Client_id INTEGER NOT NULL REFERENCES Clients(Client_id)
        );
    """)


# Функция, позволяющая добавить нового клиента
def add_client():
    cursor.execute("""
        INSERT INTO clients("name", surname) VALUES (%s, %s)
        """, (input('Введите имя клиента: '),
              input('Введите фамилию клиента: ')))
    cursor.execute("""
            SELECT client_id from clients
            ORDER BY client_id DESC
            LIMIT 1
            """)
    client_id = cursor.fetchone()[0]
    add_phone_or_email('phone', client_id)
    add_phone_or_email('email', client_id)
    print('Данные нового клиента внесены.')


# Функция, позволяющая добавить телефон или email для существующего клиента
def add_phone_or_email(command, client_id=None):
    if client_id is None:
        client_id = int(input('Введите ID клиента: '))
    cursor.execute("""
        SELECT client_id from clients
        ORDER BY client_id
    """)
    for i in cursor.fetchall():
        if client_id in i:
            if command == 'phone':
                cursor.execute("""
                    INSERT INTO phones(phone_number, client_id) VALUES (%s, %s)
                    """, (input('Введите номер телефона: '), client_id))
                return print('Номер телефона добавлен.')
            elif command == 'email':
                cursor.execute("""
                    INSERT INTO emails(email_name, client_id) VALUES (%s, %s)
                    """, (input('Введите email: '), client_id))
                return print('Email добавлен.')
    print('ОШИБКА: Клиента с таким id нет!')


# Функция, позволяющая изменить данные о клиенте
def edit():
    command = input("""Выберите, что будем менять?
        Имя - n, фамилию - s, email - e, телефон - t: """)
    if command == 'n':
        cursor.execute("""
            UPDATE clients SET name=%s WHERE client_id=%s
        """, (input('Введите новое имя: '), input('Введите id клиента: ')))
    elif command == 's':
        cursor.execute("""
            UPDATE clients SET surname=%s WHERE client_id=%s
        """, (input('Введите новую фамилию: '), input('Введите id клиента: ')))
    elif command == 'e':
        cursor.execute("""
            UPDATE emails SET email_name=%s WHERE email_name=%s
        """, (input('Введите новый email: '), input('Введите старый email: ')))
    elif command == 't':
        cursor.execute("""
            UPDATE phones SET phone_number=%s WHERE phone_number=%s
        """, (input('Введите новое имя: '), input('Введите старый телефон: ')))
    else:
        print('ОШИБКА: Неверная команда!')
        return
    print('Данные изменены!')


# Функция, позволяющая удалить телефон для существующего клиента
def del_phone():
    cursor.execute("""
        DELETE FROM phones 
        WHERE phone_number = %s
        """, (input('Введите удаляемый телефон: '),))
    print('Телефон удален!')


# Функция, позволяющая удалить существующего клиента
def del_client():
    client_id = input('Введите id клиента, которого надо удалить: ')
    cursor.execute("""
        DELETE FROM emails
        WHERE client_id = %s
    """, (client_id),)
    cursor.execute("""
        DELETE FROM phones
        WHERE client_id = %s
    """, (client_id),)
    cursor.execute("""
        DELETE FROM clients
        WHERE client_id = %s
    """, (client_id),)
    print('Данные о клиенте удалены.')


# Функция, позволяющая найти клиента по его данным
# (имени, фамилии, email-у или телефону)
def find_client():
    command = input("""Укажите параметр поиска:
        по имени - n, по фамилии - s, по emeil - e, по телефону -t: """)
    if command == 'n':
        cursor.execute("""
            select DISTINCT client_id, name, surname FROM clients 
            WHERE name = %s           
        """, (input('Введите имя клиента: '),))
    elif command == 's':
        cursor.execute("""
            select DISTINCT client_id, name, surname FROM clients
            WHERE surname = %s           
        """, (input('Введите фамилию клиента: '),))
    elif command == 'e':
        cursor.execute("""
            select DISTINCT c.client_id, c.name, c.surname FROM clients c
            JOIN emails e ON e.client_id = c.client_id
            WHERE e.email_name = %s           
        """, (input('Введите email клиента: '),))
    elif command == 't':
        cursor.execute("""
            select DISTINCT c.client_id, c.name, c.surname FROM clients c
            JOIN phones p ON p.client_id = c.client_id
            WHERE p.phone_number = %s           
        """, (input('Введите номер телефона клиента: '),))
    else:
        print('ОШИБКА: Введена неверная команда!')
        return
    print(cursor.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(
            database="dz_PostgreSQL_from_Python",
            user="postgres",
            password=input('Введите пароль от БД ')
    ) as connect:
        with connect.cursor() as cursor:
            create_bd()
            # insert_bd()
            add_client()
            add_phone_or_email('email')
            add_phone_or_email('phone')
            edit()
            del_phone()
            del_client()
            find_client()
    connect.close()
