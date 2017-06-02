import TextAnalysis
import DBconnector as DB
import Translator


all_words = TextAnalysis.get_info("english")

#DB.create_dictionary_table("Dictionary.db", "en")
#DB.insert("Dictionary.db", "en", all_words)
words = DB.select("Dictionary.db", "en", 10, 7, 'Tech')

print(Translator.translate("Shit", "en", "ru"))
