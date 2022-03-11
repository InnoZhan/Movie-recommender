import sqlite3


def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    c.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )""")


def user_check(login):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE login = '{login}'".format(login=login))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    else:
        return True


def authorization(login, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE login = '{login}' AND password = '{password}'".format(login=login,
                                                                                               password=password))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False
    else:
        return True


def registration(login, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if user_check(login):
        conn.close()
        return False

    c.execute("INSERT INTO users (login, password)VALUES ('{login}', '{password}')".format(login=login,
                                                                                           password=password))

    conn.commit()
    conn.close()
    return True


def delete_user(login):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if not user_check(login):
        conn.close()
        return False

    c.execute("DELETE FROM users WHERE login = '{login}'".format(login=login))

    conn.commit()
    conn.close()
    return True
