import sqlite3


def create():
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT,
            priority INTEGER DEFAULT 0,
            checked INTEGER DEFAULT 0)
    ''')
    
    connection.commit()
    connection.close()


def get_all():
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('SELECT name, url, priority, checked FROM item ORDER BY priority DESC')
    
    return cursor.fetchall()


def remove_checked():
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('DELETE FROM item WHERE checked = 1')

    connection.commit()
    connection.close()


def remove_all():
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('DELETE FROM item')

    connection.commit()
    connection.close()


def add(name, url):
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('INSERT INTO item (name, url) VALUES (?, ?)', (name, url))

    connection.commit()
    connection.close()


def add_priority(name):
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('SELECT priority FROM item WHERE name = ?', (name,))
    current_priority = cursor.fetchall()[0][0]
    new_priority = (current_priority + 1) % 4

    cursor.execute('UPDATE item SET priority = ? WHERE name = ?', (new_priority, name))
    
    connection.commit()
    connection.close()


def check_uncheck(name, set_to):
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()

    cursor.execute('UPDATE item SET checked = ? WHERE name = ?', (set_to, name))

    connection.commit()
    connection.close()
