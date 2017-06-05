import sqlite3

DICTIONARY_DB_NAME = "Dictionary.db"
USERS_DB_NAME = "Users.db"




def create_dictionary_table(table_name):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    t_name = (table_name)
    c.execute("CREATE TABLE if not exists {} (priority integer, word TEXT, "
              "theme TEXT, id INTEGER PRIMARY KEY)".format(t_name))
    connection.commit()
    connection.close()


def create_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.close()


def insert_dictionary(table_name, dictionary):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    for theme, info in dictionary.items():
        for word, priority in info.items():
            t_name = (table_name)
            print(priority, word, theme)
            c.execute("INSERT INTO  {} (priority, word, theme) "
                       "VALUES (?,?,?)".format(t_name), (priority, word, theme,))

    connection.commit()
    connection.close()


def select_from_dictionary(table_name, start_number, number_of_words, theme):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    command = ("SELECT word FROM {} "
               "WHERE theme='{}' "
               "ORDER BY priority DESC "
               "LIMIT {} "
               "OFFSET {}".format(table_name, theme, number_of_words, start_number))

    tuple_words = list(c.execute(command))

    list_words = list()

    for word in tuple_words:
        list_words.append(word[0])

    connection.close()
    return list_words


def create_users_db():
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    c.execute("CREATE TABLE if not exists users (chat_id integer, name TEXT, "
              "surname TEXT, native_language TEXT, second_language TEXT, progress INTEGER,  "
              "id INTEGER PRIMARY KEY)")

    connection.commit()
    connection.close()


def insert_person(chat_id, name, surname, native_language, second_langauge, progress):
    connection = sqlite3.connect("Users.db")
    c = connection.cursor()
    c.execute("INSERT INTO users (chat_id, name, surname, native_language, "
              "second_langauge, progress) "
              "VALUES (?,?,?,?,?,?)".format(chat_id, name, surname, native_language,
                                          second_langauge, progress))

    connection.commit()
    connection.close()


def contains_person(chat_id):
    connection = sqlite3.connect("Users.db")
    c = connection.cursor()
    found = c.execute("SELECT EXISTS(SELECT * FROM users WHERE chat_id = ?)", (chat_id,))

    connection.commit()
    connection.close()

    if found == 0:
        return False
    else:
        return True


