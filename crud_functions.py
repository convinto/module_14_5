import sqlite3

def initiate_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')
    connection.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

# initiate_db()

def add_user(username, email, age):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users")
    chek_user = cursor.fetchone()[0]+1
    cursor.execute(f'''
    INSERT INTO Users VALUES('{chek_user}', '{username}', '{email}', '{age}', '1000')
    ''')

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    is_inc = True
    check_usnam = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_usnam.fetchone() is None:
        is_inc = False
    connection.commit()
    connection.close()
    return is_inc




def get_all_products():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    users = cursor.fetchall()

    connection.commit()
    connection.close()
    return users

# connection = sqlite3.connect("database.db")
# cursor = connection.cursor()

# пополнение на 4 записи
# for i in range(1, 5):
#     cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)", (f'{i}', f"Product{i}", f"description{i}", 1000))
#
# connection.commit()
# connection.close()