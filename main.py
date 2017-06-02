import TextAnalysis
import DBconnector as DB


all_words = TextAnalysis.get_info()

DB.create_dictionary_table("Dictionary.db", "en")
DB.insert("Dictionary.db", "en", all_words)
