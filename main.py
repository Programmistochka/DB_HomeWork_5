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

def add_person (firstname, name, e_mail, num_phones):
    cur.execute("""
        INSERT INTO clients(firstname, name, e_mail) VALUES(%s, %s, %s);
        """, (firstname, name, e_mail))
    
    cur.execute("""
        SELECT client_id FROM clients WHERE firstname=%s AND name =%s;
        """, (firstname, name)) 
    client_id = cur.fetchone()[0]
    print(client_id)
    
    for phone in num_phones:
        cur.execute("""
            INSERT INTO phones(number, client_id) VALUES(%s, %s);
            """, (phone, client_id))

        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())
        cur.execute("""
            SELECT * FROM phones;
            """)
        print(cur.fetchall())
    conn.commit()  # фиксируем в БД    

def line(n=10):
    print('---'*n)

if __name__ == "__main__":
 while True:
    
    with psycopg2.connect(database="dbhomework5", user="postgres", password="Adminik") as conn:
        with conn.cursor() as cur:   
            create_tables(cur)
            user_comand = input('Введите команду:\n 1 - добавить нового клиента\n 2 - добавить телефон для существующего клиента\n 3 - изменить данные о клиенте\n 4 - удалить телефон для существующего клиента\n 5 - найти клиента по его данным (имени, фамилии, email или телефону)\n - - - - - - - \n q - выход\n')
            if user_comand == '1':
                line()
                print('Введите данные по клиенту: ')
                name = input('Имя - ')
                firstname = input('Фамилия - ')
                email = input('email - ')
                q_phone = int(input('Сколько номеров телефонов хотите добавить: '))
                phone = []
                for i in range(q_phone):
                    input_phone = input('Введите номер')
                    phone.append(input_phone)
                add_person (firstname, name, email, phone)
                print(f'Клиент {firstname} {name} добавлен') 
                line()
            elif user_comand == '2':
                line()
                add_person('Сомов','Михаил', 'somov@mail.ru', '8-914-900-45-57')
                add_person('Ермаков','Михаил', 'ermakov@mail.ru', '8-914-900-75-50')
                add_person('Соколова','Аня', 'sokolova@mail.ru', '8-914-900-05-59')
            elif user_comand == 'q':
                print('До свидания!')
                break
            else:
                print('Такой команды нет, попробуйте еще раз!')