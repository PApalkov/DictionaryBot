import sqlite3

DICTIONARY_DB_NAME = "./Dictionary.db"
USERS_DB_NAME = "./Users.db"


#todo привести в нормальный вид
#===============DICTIONARY PART===============


def create_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.close()


def create_dictionary_table(table_name):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    t_name = (table_name)
    c.execute("CREATE TABLE if not exists {} (priority integer, word TEXT, "
              "theme TEXT, id INTEGER PRIMARY KEY)".format(t_name))
    connection.commit()
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


#=================USERS PART===============

def create_users_db():
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    c.execute("CREATE TABLE if not exists users (chat_id integer, name TEXT, "
              "surname TEXT, first_language TEXT, second_language TEXT, progress INTEGER, "
              "registration_step INTEGER, theme TEXT, id INTEGER PRIMARY KEY)")

    connection.commit()
    connection.close()

def contains_person(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    found = c.execute("SELECT EXISTS(SELECT * FROM users WHERE chat_id = ?)", (chat_id,)).fetchall()

    connection.commit()
    connection.close()

    print(found)
    if found[0] == (0,):
        return False
    else:
        return True


def insert_person(chat_id, name, surname, registration_step):
    connection = sqlite3.connect("Users.db")
    c = connection.cursor()
    c.execute("INSERT INTO users (chat_id, name, surname, registration_step, progress)"
              "VALUES (?,?,?,?,?)", (chat_id, name, surname, registration_step, 0))

    connection.commit()
    connection.close()


def set_first_language(chat_id, fisrt_language):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    c.execute("UPDATE users SET first_language = ? "
              "WHERE chat_id=?", (fisrt_language, chat_id,))

    connection.commit()
    connection.close()


def set_second_language(chat_id, second_language):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    c.execute("UPDATE users SET second_language = '{}' "
              "WHERE chat_id={}".format(second_language, chat_id))

    connection.commit()
    connection.close()


def set_theme(chat_id, theme):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()
    c.execute("UPDATE users SET theme = '{}' "
              "WHERE chat_id={}".format(theme, chat_id))

    connection.commit()
    connection.close()


def inc_progress(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    c.execute("UPDATE users SET progress = progress + 10 "
              "WHERE chat_id={}".format(chat_id))

    connection.commit()
    connection.close()


def inc_reg_step(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    c.execute("UPDATE users SET registration_step = registration_step + 1 "
              "WHERE chat_id={}".format(chat_id))

    connection.commit()
    connection.close()


def get_reg_step(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    rp = c.execute("SELECT registration_step FROM users WHERE chat_id = ?", (chat_id,)).fetchall()

    connection.commit()
    connection.close()

    return rp[0][0]

def get_progress(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    pr = c.execute("SELECT progress FROM users WHERE chat_id = ?", (chat_id,)).fetchall()

    connection.commit()
    connection.close()

    return pr[0][0]



def get_first_language(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    fl = c.execute("SELECT first_language FROM users "
                   "WHERE chat_id = ?", (chat_id,)).fetchall()

    connection.commit()
    connection.close()

    return fl[0][0]


def get_second_language(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    sl = c.execute("SELECT second_language FROM users "
                   "WHERE chat_id = ?", (chat_id,)).fetchall()

    connection.commit()
    connection.close()

    return sl[0][0]


def get_theme(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    th = c.execute("SELECT theme FROM users "
                   "WHERE chat_id = ?", (chat_id,)).fetchall()

    connection.commit()
    connection.close()


    return th[0][0]

def del_person(chat_id):
    connection = sqlite3.connect(USERS_DB_NAME)
    c = connection.cursor()

    c.execute("DELETE FROM users "
                   "WHERE chat_id = ?", (chat_id,))

    connection.commit()
    connection.close()
