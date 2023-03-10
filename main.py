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
        
        #client_phones = cur.fetchall()
    conn.commit()
    print(f'Телефоны {numbs_phone} добавлены')
    return cur

def update_client_info():
  pass
   

def all_clients(conn): 
    #with conn.cursor() as cur:
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
                user_comand = input('Введите команду:\n 1 - создать новую БД\n 2 - добавить нового клиента\n 3 - добавить телефон для существующего клиента\n 4 - изменить данные о клиенте\n 5 - удалить телефон для существующего клиента\n 6 - найти клиента по его данным (имени, фамилии, email или телефону)\n 7 - просмотеть данные по всем клиентам\n - - - - - - - \n q - выход\n')
                if user_comand == '1':
                    create_tables(cur)
                elif user_comand == '2':
                    line()
                    print('Введите данные по клиенту ')
                    name = input('Имя: ')
                    firstname = input('Фамилия: ')
                    email = input('email: ')
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
                    f_name = input('Имя: ')
                    f_firstname = input('Фамилия:')
                    q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                    for i in range(q_phone):
                        input_phone = input('Введите номер: ')
                        phones.append(input_phone)
                    add_phones_by_id(cur, get_client_id(cur, f_firstname, f_name), phones)
                elif user_comand == '7':
                    line()
                    all_clients(cur)
                elif user_comand == 'q':
                    conn.close()
                    print('До свидания!')
                    break
                else:
                    print('Такой команды нет, попробуйте еще раз!')