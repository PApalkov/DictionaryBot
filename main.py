import TextAnalysis
import DBconnector as DB
from Translator import translate


#all_words = TextAnalysis.get_info("english")

DB.create_dictionary_table("fr")
#DB.insert_dictionary("en", all_words)
words = DB.select_from_dictionary("en", 0, 10, 'TECH')
print(words)
#DB.create_users_db()

#for i, word in enumerate(words):
#    print(i, word,'-', translate(word, "en", "ru"))
