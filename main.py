import TextAnalysis
import DBconnector as DB


all_words, special_words = TextAnalysis.get_info()

DB.create_dictionary_table("Dictionary.db", "AllWords")
DB.insert("Dictionary.db", "AllWords", all_words)


for theme, words in special_words:
    DB.create_dictionary_table("Dictionary.db", theme)
    DB.insert("Dictionary.db", theme, words)
