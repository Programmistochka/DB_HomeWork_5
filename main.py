import psycopg2

with psycopg2.connect(database="dbhomework5", user="postgres", password="Adminik") as conn:
    with conn.cursor() as cur:
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
            e_mail VARCHAR(40) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            phone_id SERIAL PRIMARY KEY,
            number VARCHAR(20) UNIQUE,
            client_id INTEGER NOT NULL REFERENCES clients(client_id)
        );
        """)
        conn.commit() #фиксирует изменения в бд

    # наполнение таблиц (C из CRUD)
        cur.execute(""" INSERT INTO clients(client_id, firstname, name, e_mail) VALUES (1, 'Петров', 'Олег', 'petrov@mail.ru')
        """)
    
        cur.execute(""" INSERT INTO clients(client_id, firstname, name, e_mail) VALUES (2, 'Сомова', 'Алина', 'somova@mail.ru')
        """)
        
        cur.execute("""
        SELECT * FROM clients;
        """)
        print('fetchall', cur.fetchall())  
        # cur.execute("""
        # INSERT INTO homework(number, description, course_id) VALUES(1, 'простое дз', 1);
        # """)
        # conn.commit()  # фиксируем в БД

        # # извлечение данных (R из CRUD)
        # cur.execute("""
        # SELECT * FROM course;
        # """)
        # print('fetchall', cur.fetchall())  # извлечь все строки

        # cur.execute("""
        # SELECT * FROM course;
        # """)
        # print(cur.fetchone())  # извлечь первую строку (аналог LIMIT 1)

        # #Правильный способ поиска значения с использованием sql-запроса (во избежание sql-инъекций)
        # cur.execute("""
        # SELECT id FROM course WHERE name=%s;
        # """, ("Python",))  # правильно, обратите внимание на кортеж
        # print(cur.fetchone())

        # def get_course_id(cursor, name: str) -> int:
        #     cursor.execute("""
        #     SELECT id FROM course WHERE name=%s;
        #     """, (name,))
        #     return cur.fetchone()[0]
        # python_id = get_course_id(cur, 'Python')
        # print('python_id', python_id)




conn.close()