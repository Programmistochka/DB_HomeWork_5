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

    
    
def get_client_id(cur, firstname = None, name = None, email = None):
    if firstname == ' ' or firstname == '':
        firstname = None
    if name == ' ' or name == '':
        name = None
    if email == ' ' or email == '':
        email = None    

    if email is None:
        if firstname is None:
            if name is None:
                print(f'Нет данных для поиска')
                client_id = None
            else:
                #email = None, firstname = None, name <> None
                cur.execute("""
                   SELECT client_id FROM clients WHERE name = %s;
                """, (name,))
                rez = cur.fetchall()
                #print(f'Результат поиска по имени {rez}')
        else:
            #email = None, firstname <> None
            if name is None:
                cur.execute("""
                SELECT client_id FROM clients WHERE firstname = %s;
                """, (firstname,))
                rez = cur.fetchall()
                #print(f'Результат поиска по фамили {rez}')
            else:
                #email = None, firstname <> None, name <> None
                cur.execute("""
                SELECT client_id FROM clients WHERE firstname = %s and name = %s;
                """, (firstname, name))
                rez = cur.fetchall()
                #print(f'Результат поиска по имени и фамили {rez}')
    else:
        #email <> None
        #email поле с уникальными значениями, поэтому, если он указан можно искать исключительно по нему
        cur.execute("""SELECT * FROM clients WHERE e_mail = %s;
            """, (email,))
        rez = cur.fetchall()
        #print(f'Результат поиска по email {rez}')
        if len(rez)==1 and firstname is not None and firstname != str(rez[0][1]):
           print(f'ВНИМАНИЕ! Данные по фамилии {firstname}/{rez[0][1]} не соответствуют записи найденной по email: {email}')
        if len(rez)==1 and name is not None and name != rez[0][2]:
           print(f'ВНИМАНИЕ! Данные по имени {name}/{rez[0][2]} не соответствуют записи найденной по email: {email}')

    #обработка результатов запроса
    line()
    if len(rez) == 1:
        #print('Найдено одно совпадение: ', rez)
        client_id = rez[0][0]    
    elif len(rez) > 1:
        print('Найдено несколько совпадений. Не достаточно данных. Повторите попытку')
        client_id = None
    else:
        print('Клиент не найден в базе данных')
        client_id = None

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

def del_client(cur, client_id):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
    
    cur.execute("""
        DELETE FROM clients WHERE client_id=%s;
        """, (client_id,))
        
    print(f'Клиент id {client_id} удален из базы данных')


def del_phone_by_number(cur, number):
    #number - поле с уникальными значениями
    
    cur.execute("""
        SELECT number FROM phones WHERE number=%s;
        """, (number,))
    find_phone = cur.fetchall()
    if len(find_phone) == 1:
        cur.execute("""
            DELETE FROM phones WHERE number=%s;
            """, (number,))
        print(f'Телефон {number} удален из базы данных')
    else:
        print(f'Телефон {number} не найден в базе данных')

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
                    if firstname == '' or name == '' or email == '':
                        print('Добавление клиента не возможно. Все значения должны быть заполнены')
                    else:
                        if get_client_id(cur, firstname, name, email) is None:
                            q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                            phones = []
                            for i in range(q_phone):
                                input_phone = input('Введите номер: ')
                                phones.append(input_phone)
                            add_person (cur, firstname, name, email, phones)
                        else:
                            print('Такой клиент уже есть в базе данных')
                    line()
                elif user_comand == '3':
                    line()
                    phones = []
                    print('Для добавления телефона укажите')
                    f_firstname = (input('Фамилия: ')).title()
                    f_name = (input('Имя: ')).title()
                    client_id = get_client_id(cur, f_firstname, f_name)
                    if client_id != None:
                        q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                        for i in range(q_phone):
                            input_phone = input('Введите номер: ')
                            phones.append(input_phone)
                            add_phones_by_id(cur, client_id, phones)
                    else:
                        print('Добавление телефона невозможно. Повторите попытку.')
                    line()
                elif user_comand == '5':
                    line()
                    phone = input('Для удаления укажите номер телефона: ')
                        
                    del_phone_by_number(cur, phone)
                    line()
                elif user_comand == '6':
                    line()
                    print('Для удаления укажите')
                    f_firstname = (input('Фамилия: ')).title()
                    f_name = (input('Имя: ')).title()
                    f_email = (input('email: ')).lower()
                    client_id = get_client_id(cur, f_firstname, f_name, f_email)
                    if client_id is not None:
                        del_client(cur, client_id)
                    line()
                elif user_comand == '7':
                    line()
                    print('Для поиска укажите')
                    f_firstname = (input('Фамилия: ')).title()
                    f_name = (input('Имя: ')).title()
                    f_email = (input('email: ')).lower()
                    client_id = get_client_id(cur, f_firstname, f_name, f_email) 
                    if client_id is not None:
                        print(f'Клиент найден: client_id = {client_id}')
                    line()
                elif user_comand == '8':
                    line()
                    all_clients(cur)
                    line()
                elif user_comand == 'q':
                    conn.close()
                    print('До свидания!')
                    break
                else:
                    line()
                    print('Такой команды нет, попробуйте еще раз!')
                    line()