from telebot import types

ENGLISH_LANGUAGE = "ENGLISH"
RUSSIAN_LANGUAGE = "RUSSIAN"
FRENCH_LANGUAGE = "FRENCH"
GERMAN_LANGUAGE = "GERMAN"


def make_language_keyboard(first_language = None):

    languages = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    english = types.KeyboardButton(ENGLISH_LANGUAGE)
    french = types.KeyboardButton(FRENCH_LANGUAGE)
    german = types.KeyboardButton(GERMAN_LANGUAGE)
    russian = types.KeyboardButton(RUSSIAN_LANGUAGE)

    if first_language == ENGLISH_LANGUAGE:
        languages.add(russian, french, german)

    elif first_language == RUSSIAN_LANGUAGE:
        languages.add(english, french, german)

    elif first_language == FRENCH_LANGUAGE:
        languages.add(english, russian, german)

    elif first_language == GERMAN_LANGUAGE:
        languages.add(english, russian, french)

    else:
        languages.add(english, russian, french, german)

    return languages


def make_theme_keyboard():

    themes = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    common = types.KeyboardButton("COMMON")
    tech = types.KeyboardButton("TECH")
    medicine = types.KeyboardButton("MEDICINE")
    legal = types.KeyboardButton("LEGAL")

    themes.add(common, tech, medicine, legal)
    return themes


def send_words_keyboard():

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    get_words = types.KeyboardButton("GET WORDS")
    back = types.KeyboardButton("BACK")
    keyboard.add(get_words, back)

    return keyboard


def get_intro_message():
    with open("intro.txt", 'r') as fp:
        intro_message = ""
        for row in fp:
            intro_message += row

        return intro_message

