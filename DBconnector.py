import sqlite3
from Translator import translate

DICTIONARY_DB_NAME = "./Dictionary.db"
USERS_DB_NAME = "./Users.db"


def db_execute(db_name, command):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()
    c.execute(command)
    connection.commit()
    connection.close()


def db_execute_feedback(db_name, command):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    result = c.execute(command).fetchall()

    connection.commit()
    connection.close()

    return result[0][0]


#todo привести в нормальный вид
#===============DICTIONARY PART===============


def create_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.close()


def create_dictionary_table(table_name):
    command = "CREATE TABLE if not exists {} " \
              "(id INTEGER PRIMARY KEY," \
              "priority integer, " \
              "en TEXT, " \
              "ru TEXT, " \
              "fr TEXT, " \
              "de TEXT, " \
              "theme TEXT)".format(table_name)

    db_execute(DICTIONARY_DB_NAME, command)

'''
def insert_dictionary(table_name, dictionary):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    for theme, info in dictionary.items():
        for word, priority in info.items():
            t_name = (table_name)
            print(priority, word, theme)
            c.execute("INSERT INTO  {} "
                      "(priority, word, theme) "
                      "VALUES (?,?,?)".format(t_name), (priority, word, theme,))

    connection.commit()
    connection.close()
'''


def insert_dictionary_translating(table_name, dictionary):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    for theme, info in dictionary.items():
        for en_word, priority in info.items():
            if len(en_word) > 2:

                print(en_word)
                ru_word = translate(en_word, "en", "ru")
                fr_word = translate(en_word, "en", "fr")
                de_word = translate(en_word, "en", "de")

                c.execute("INSERT INTO  {} "
                          "(priority, "
                          "en, "
                          "ru, "
                          "fr, "
                          "de,"
                          "theme) "
                          "VALUES (?,?,?,?,?,?)".format(table_name),
                          (priority, en_word, ru_word, fr_word, de_word, theme,))

    connection.commit()
    connection.close()


def select_from_dictionary(first_language, second_language, start_number,
                           number_of_words, theme):
    connection = sqlite3.connect(DICTIONARY_DB_NAME)
    c = connection.cursor()

    command = "SELECT {}, {} " \
              "FROM words " \
              "WHERE theme='{}' " \
              "ORDER BY priority DESC " \
              "LIMIT {} " \
              "OFFSET {}".format(first_language, second_language, theme,
                                 number_of_words, start_number)

    tuple_words = list(c.execute(command))

    list_words = list()

    for word in tuple_words:
        line = word[1] + " - " + word[0] + "\n"
        list_words.append(line)

    connection.close()
    return list_words


#=================USERS PART===============

def create_users_db():
    command = "CREATE TABLE if not exists users " \
               "(chat_id integer, " \
               "first_language TEXT, " \
               "second_language TEXT, " \
               "COMMON INTEGER, " \
               "TECH INTEGER, " \
               "MEDICINE INTEGER, " \
               "LEGAL INTEGER, " \
               "registration_step INTEGER, " \
               "theme TEXT, " \
               "id INTEGER PRIMARY KEY)"

    db_execute(USERS_DB_NAME, command)


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
    command = "INSERT INTO users " \
              "(chat_id, registration_step, COMMON," \
              "TECH, MEDICINE, LEGAL)" \
              " VALUES ({}, {}, {}, {} ,{}, {})".format(chat_id, registration_step,
                                                        0, 0, 0, 0)

    db_execute(USERS_DB_NAME, command)


def set_first_language(chat_id, fisrt_language):
    command = "UPDATE users SET first_language = '{}' " \
              "WHERE chat_id={}".format(fisrt_language, chat_id)

    db_execute(USERS_DB_NAME, command)


def set_second_language(chat_id, second_language):
    command =  "UPDATE users " \
               "SET second_language = '{}' " \
               "WHERE chat_id={}".format(second_language, chat_id)

    db_execute(USERS_DB_NAME, command)


def set_theme(chat_id, theme):
    command =  "UPDATE users " \
               "SET theme = '{}' " \
               "WHERE chat_id={}".format(theme, chat_id)

    db_execute(USERS_DB_NAME, command)


def inc_progress(chat_id):
    theme = get_theme(chat_id)
    print(theme)
    command =  "UPDATE users " \
               "SET {} = {} + 10 " \
               "WHERE chat_id={}".format(theme, theme,  chat_id)

    db_execute(USERS_DB_NAME, command)


def inc_reg_step(chat_id):
    command =  "UPDATE users " \
               "SET registration_step = registration_step + 1 " \
               "WHERE chat_id={}".format(chat_id)

    db_execute(USERS_DB_NAME, command)


def dec_reg_step(chat_id):
    command =  "UPDATE users " \
               "SET registration_step = registration_step - 1 " \
               "WHERE chat_id={}".format(chat_id)

    db_execute(USERS_DB_NAME, command)


def get_reg_step(chat_id):
    command =  "SELECT registration_step " \
               "FROM users " \
               "WHERE chat_id = {}".format(chat_id)

    return db_execute_feedback(USERS_DB_NAME, command)


def get_progress(chat_id):
    theme = get_theme(chat_id)

    command =  "SELECT {} " \
               "FROM users " \
               "WHERE chat_id = {}".format(theme, chat_id)

    return db_execute_feedback(USERS_DB_NAME, command)


def get_first_language(chat_id):
    command = "SELECT first_language " \
               "FROM users " \
               "WHERE chat_id = {}".format(chat_id)

    return db_execute_feedback(USERS_DB_NAME, command)


def get_second_language(chat_id):
    command =  "SELECT second_language " \
               "FROM users " \
               "WHERE chat_id = {}".format(chat_id)

    return db_execute_feedback(USERS_DB_NAME, command)


def get_theme(chat_id):
    command =  "SELECT theme " \
               "FROM users " \
               "WHERE chat_id = {}".format(chat_id)

    return db_execute_feedback(USERS_DB_NAME, command)


def del_person(chat_id):
    command = "DELETE FROM users " \
              "WHERE chat_id = {}".format(chat_id)

    db_execute(USERS_DB_NAME, command)

