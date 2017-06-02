import sqlite3
#todo make bd with names of themes


def create_dictionary_table(db_name, table_name):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    t_name = (table_name)
    c.execute("CREATE TABLE if not exists {} (priority integer, word TEXT, "
              "theme TEXT, id INTEGER PRIMARY KEY)".format(t_name))
    connection.commit()
    connection.close()


def create_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.close()


def insert(db_name, table_name, dictionary):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    for theme, info in dictionary.items():
        for word, priority in info.items():

            t_name = (table_name)

            c.execute("INSERT INTO  {} (priority, word, theme) "
                       "VALUES (?,?,?)".format(t_name), (priority, word, theme,))

    connection.commit()
    connection.close()


def select(db_name, table_name, start_number, number_of_words, theme):
    connection = sqlite3.connect(db_name)
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
