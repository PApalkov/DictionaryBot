import TextAnalysis
import DBconnector as DB
from Translator import translate


all_words = TextAnalysis.get_info("english")

#DB.create_dictionary_table("en")
#DB.insert_dictionary("en", all_words)
words = DB.select_from_dictionary("en", 52, 10, 'Tech')

for i, word in enumerate(words):
    print(i, word,'-', translate(word, "en", "ru"))
