import sqlite3

def create_dictionary_table(db_name, table_name):

    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    #creating table
    command = ("CREATE TABLE " + table_name + " (N integer, key text, value text)")
    print(command)
    c.execute(command)

    #saving changes
    connection.commit()

    #closing DB
    connection.close()





if __name__ == "__main__":
    create_dictionary_table("Dictionary.db", "en_ru")