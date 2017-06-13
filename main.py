import TextAnalysis
import DBconnector as DB
from Translator import translate


"""
all_words = TextAnalysis.get_info("english")

DB.create_dictionary_table("words")

DB.insert_dictionary_translating("words", all_words)

words = DB.select_from_dictionary("ru", "en", 0, 10, 'TECH')
print(words)
"""
DB.create_users_db()

