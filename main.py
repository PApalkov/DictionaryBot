import TextAnalysis
import DBconnector as DB
from Translator import translate


all_words = TextAnalysis.get_info("russian")

#DB.create_dictionary_table("fr")
DB.insert_dictionary("ru", all_words)
words = DB.select_from_dictionary("ru", 0, 10, 'TECH')
print(words)
#DB.create_users_db()

#for i, word in enumerate(words):
#    print(i, word,'-', translate(word, "en", "ru"))
