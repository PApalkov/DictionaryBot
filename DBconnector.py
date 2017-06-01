import sqlite3

def create_dictionary_table(db_name, table_name):

    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    #creating table
    command = ("CREATE TABLE " + table_name + " (priority integer, word text)")

    c.execute(command)

    #saving changes
    connection.commit()

    #closing DB
    connection.close()


def create_db(db_name):

    connection = sqlite3.connect(db_name)
    connection.close()


def insert(db_name, table_name, priority, word):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    #inserting
    command = ("INSERT INTO " + table_name + " VALUES (" + str(priority) + ",'" + word + "')")

    c.execute(command)

    # saving changes
    connection.commit()

    # closing DB
    connection.close()

def insert(db_name, table_name, dictionary):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    print(dictionary)
    for word, priority in dictionary.items():
        # inserting
        command = ("INSERT INTO " + table_name + " VALUES (" + str(priority) + ",'" + word + "')")

    c.execute(command)

    #command = ("ORDER BY " + table_name + " priority")

    c.execute(command)

    # saving changes
    connection.commit()

    # closing DB
    connection.close()

#todo make selection
if __name__ == "__main__":
    create_dictionary_table("Dictionary.db", "en_ru")
    insert("Dictionary.db", "en_ru", 5, "Danya")