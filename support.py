from telebot import types


def make_language_keyboard(first_language = None):

    languages = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    english = types.KeyboardButton("ENGLISH")
    french = types.KeyboardButton("FRENCH")
    german = types.KeyboardButton("GERMAN")
    russian = types.KeyboardButton("RUSSIAN")

    if first_language == "ENGLISH":
        languages.add(russian, french, german)

    elif first_language == "RUSSIAN":
        languages.add(english, french, german)

    elif first_language == "FRENCH":
        languages.add(english, russian, german)

    elif first_language == "GERMAN":
        languages.add(english, russian, french)

    else:
        languages.add(english, russian, french, german)

    return languages


def make_theme_keyboard():

    themes = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    common = types.KeyboardButton("COMMON")
    tech = types.KeyboardButton("TECH")
    medicine = types.KeyboardButton("MEDICINE")
    #legal = types.KeyboardButton("LEGAL")

    themes.add(common, tech, medicine, '''legal''')
    return themes


def get_intro_message():
    with open("intro.txt", 'r') as fp:
        intro_message = ""
        for row in fp:
            intro_message += row

        return intro_message

