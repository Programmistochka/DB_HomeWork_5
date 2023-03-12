# -*- coding: utf-8 -*-
import psycopg2

def create_tables(cur):
    # удаление таблиц
    cur.execute("""
        DROP TABLE IF EXISTS phones;
        DROP TABLE IF EXISTS clients;
    """)    
        
    # создание таблиц
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        firstname VARCHAR(40) NOT NULL,
        name VARCHAR(40) NOT NULL,
        e_mail VARCHAR(40) UNIQUE NOT NULL 
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        phone_id SERIAL PRIMARY KEY,
        number VARCHAR(20) UNIQUE NOT NULL,
        client_id INTEGER NOT NULL REFERENCES clients(client_id)
        );
    """)

    conn.commit()
    all_clients(cur)

def add_person (cur, firstname, name, e_mail, numbs_phone = None):
    #with conn.cursor() as cur:
    cur.execute("""
        INSERT INTO clients(firstname, name, e_mail) VALUES(%s, %s, %s);
        """, (firstname, name, e_mail))
    conn.commit()
    if numbs_phone is not None:
        add_phones_by_id(cur, get_client_id(cur, firstname, name), numbs_phone)
   
    print(f'Клиент {firstname} {name} добавлен')

    
    
def get_client_id(cur, firstname, name = None):
    #with conn.cursor() as cur:
    if name == None:
        cur.execute("""
            SELECT client_id FROM clients WHERE firstname = %s;
            """, (firstname))
        client_id = cur.fetchall()
        if len(client_id) > 1:
            error_msg = 'В БД есть однофамильцы, уточните имя клиента и повторите запрос'
            return error_msg
           
    else:
        cur.execute("""
            SELECT client_id FROM clients WHERE firstname = %s AND name = %s;
            """, (firstname, name)) 
    client_id = cur.fetchone()[0]
    if client_id is None:
            error_msg = 'Такого клиента нет в БД'
            return error_msg
    print(f'client_id {client_id}')
    return client_id
    
   
    
def add_phones_by_id(cur, client_id, numbs_phone):
    #with conn.cursor() as cur:    
    for phone in numbs_phone:
        cur.execute("""
            INSERT INTO phones(number, client_id) VALUES(%s, %s);
            """, (phone, client_id))
    conn.commit()
    print(f'Телефоны {numbs_phone} добавлены')
    return cur

def update_client_info():
    pass

def find_person_by_info(cur, firstname = None, name = None, email = None):
    pass


def all_clients(conn): 
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())
            
    cur.execute("""
        SELECT * FROM phones;
        """)
    print(cur.fetchall())
            

def line(n=10):
    print('---'*n)

if __name__ == "__main__":
    while True:
        with psycopg2.connect(database="dbhomework5", user="postgres", password="Adminik") as conn:
            with conn.cursor() as cur:   
                user_comand = input('Введите команду:\n 1 - создать новую БД\n 2 - добавить нового клиента\n 3 - добавить телефон для существующего клиента\n 4 - изменить данные о клиенте\n 5 - удалить телефон для существующего клиента\n 6 - удалить существующего клиента\n 7 - найти клиента по его данным (имени, фамилии, email или телефону)\n 8 - просмотеть данные по всем клиентам\n - - - - - - - \n q - выход\n')
                if user_comand == '1':
                    create_tables(cur)
                elif user_comand == '2':
                    line()
                    print('Введите данные по клиенту ')
                    firstname = (input('Фамилия: ')).title()
                    name = (input('Имя: ')).title()
                    email = (input('email: ')).lower()
                    q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                    phones = []
                    for i in range(q_phone):
                        input_phone = input('Введите номер: ')
                        phones.append(input_phone)
                    add_person (cur, firstname, name, email, phones)
                    line()
                elif user_comand == '3':
                    line()
                    phones = []
                    print('Для добавления телефона укажите')
                    f_firstname = (input('Фамилия: ')).title()
                    f_name = (input('Имя: ')).title()
                    cur.execute("""SELECT * FROM clients WHERE firstname = %s and name = %s;
                        """, (f_firstname, f_name))
                    rez = cur.fetchall()
                    print(f'Результат поиска по фамилии и имени: {rez} len {len(rez)} id {rez[0][0]}')
                    if len(rez) == 1:
                        q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                        for i in range(q_phone):
                            input_phone = input('Введите номер: ')
                            phones.append(input_phone)
                        add_phones_by_id(cur, rez[0][0], phones)
                    elif len(rez) == 0:
                        print('В БД нет такого клиента')
                    else:
                        email = (input('В БД данных есть несколько клиентов с такими данными, введите email: ')).lower()
                        cur.execute("""SELECT * FROM clients WHERE e_mail = %s;
                        """, (email,))
                        rez = cur.fetchall()
                        print(f'Результат поиска по email {rez}')
                        if len(rez) == 1:
                            q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                            for i in range(q_phone):
                                input_phone = input('Введите номер: ')
                                phones.append(input_phone)
                                add_phones_by_id(cur, rez[0][0], phones)
                        else:
                            print('Клиента с таким email в БД нет')
                elif user_comand == '8':
                    line()
                    all_clients(cur)
                elif user_comand == 'q':
                    conn.close()
                    print('До свидания!')
                    break
                else:
                    print('Такой команды нет, попробуйте еще раз!')