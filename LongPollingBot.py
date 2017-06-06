import telebot
from config import token
import DBconnector as DB
import support
from Translator import translate


#Registration Steps
CHOOSING_FIRST_LANGUAGE = 0
CHOOSING_SECOND_LANGUAGE = 1
CHOOSING_THEME = 2
FINISHED = 3

ENGLISH_LANGUAGE = "ENGLISH"
RUSSIAN_LANGUAGE = "RUSSIAN"
FRENCH_LANGUAGE = "FRENCH"
GERMAN_LANGUAGE = "GERMAN"

COMMON_THEME = "COMMON"
TECH_THEME = "TECH"
MED_THEME = "MEDICINE"
LEGAL_THEME = "LEGAL"


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    #todo send introduction message

    chat = message.chat
    if not(DB.contains_person(chat.id)):
        print(chat)
        id = chat.id
        name = chat.first_name
        last_name = chat.last_name
        registration_step = CHOOSING_FIRST_LANGUAGE
        DB.insert_person(id, name, last_name, registration_step)


        lang_keyboard = support.make_language_keyboard()
        bot.send_message(chat_id=chat.id, text="Choose your language:", reply_markup=lang_keyboard)
    else:
        send_words(message)


@bot.message_handler(commands=['stop'])
def last_message(message):
    del_keyboard = telebot.types.ReplyKeyboardRemove()
    DB.del_person(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Bye!", reply_markup=del_keyboard)


def send_words(message):
    if message.text == "GET WORDS":
        chat_id = message.chat.id

        first_language = DB.get_first_language(chat_id)
        second_language = DB.get_second_language(chat_id)
        progress = DB.get_progress(chat_id)
        theme = DB.get_theme(chat_id)

        if second_language == "en": print("ЗАЛУПА")
        else: print(second_language)

        words = DB.select_from_dictionary(second_language, progress, 10, theme)

        print(words)
        print(first_language, second_language, progress, theme)

        translated_words = ""

        if len(words) > 0:
            for word in words:
                translation = translate(word, second_language, first_language)

                #if the word is rubbish
                if not(word == translation):
                    translated_words += word + " - " + translation + "\n"

            print(translated_words)

            DB.inc_progress(chat_id)

            bot.send_message(chat_id, translated_words)
        else:
            bot.send_message(chat_id, "You have finished this part!")


def set_first_language (message):
    chat_id = message.chat.id
    language = message.text

    if language == ENGLISH_LANGUAGE:
        DB.set_first_language(chat_id, "en")
        lang_keyboard = support.make_language_keyboard(ENGLISH_LANGUAGE)
        bot.send_message(chat_id=chat_id, text="Choose the language you are learning:",
                         reply_markup=lang_keyboard)

    elif language == GERMAN_LANGUAGE:
        DB.set_first_language(chat_id, "de")
        lang_keyboard = support.make_language_keyboard(GERMAN_LANGUAGE)
        bot.send_message(chat_id=chat_id, text="Choose the language you are learning:",
                         reply_markup=lang_keyboard)

    elif language == RUSSIAN_LANGUAGE:
        DB.set_first_language(chat_id, "ru")
        lang_keyboard = support.make_language_keyboard(RUSSIAN_LANGUAGE)
        bot.send_message(chat_id=chat_id, text="Choose the language you are learning:",
                         reply_markup=lang_keyboard)

    elif language == FRENCH_LANGUAGE:
        DB.set_first_language(chat_id, "fr")
        lang_keyboard = support.make_language_keyboard(FRENCH_LANGUAGE)
        bot.send_message(chat_id=chat_id, text="Choose the language you are learning:",
                         reply_markup=lang_keyboard)

    else:
        lang_keyboard = support.make_language_keyboard()
        bot.send_message(chat_id=chat_id, text="Choose your language:",
                         reply_markup=lang_keyboard)


def set_second_language(message):
    chat_id = message.chat.id
    language = message.text

    theme_keyboard = support.make_theme_keyboard()

    if language == ENGLISH_LANGUAGE:
        DB.set_second_language(chat_id, "en")
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)

    elif language == GERMAN_LANGUAGE:
        DB.set_second_language(chat_id, "de")
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)

    elif language == RUSSIAN_LANGUAGE:
        DB.set_second_language(chat_id, "ru")
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)

    elif language == FRENCH_LANGUAGE:
        DB.set_second_language(chat_id, "fr")
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)

    else:
        first_language = DB.get_first_language(chat_id)
        lang_keyboard = support.make_language_keyboard(first_language)
        bot.send_message(chat_id=chat_id, text="Choose the language you are learning:",
                         reply_markup=lang_keyboard)


def set_theme(message):
    chat_id = message.chat.id
    theme = message.text

    send_words_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    send_words_keyboard.add("GET WORDS")


    if theme == COMMON_THEME:
        DB.set_theme(chat_id, COMMON_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)
        send_words(message)

    elif theme == TECH_THEME:
        DB.set_theme(chat_id, TECH_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)
        send_words(message)

    elif theme == MED_THEME:
        DB.set_theme(chat_id, MED_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)
        send_words(message)

    elif theme == LEGAL_THEME:
        DB.set_theme(chat_id, LEGAL_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)
        send_words(message)

    else:
        theme_keyboard = support.make_theme_keyboard()
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)



@bot.message_handler(func=lambda m: True)
def usual_messages(message):
    chat_id = message.chat.id

    if (DB.contains_person(chat_id)):

        if DB.get_reg_step(chat_id) == FINISHED:
            send_words(message)

        elif DB.get_reg_step(chat_id) == CHOOSING_FIRST_LANGUAGE:
            print("GOT HERE")
            set_first_language(message)
            DB.inc_reg_step(chat_id)

        elif DB.get_reg_step(chat_id) == CHOOSING_SECOND_LANGUAGE:
            set_second_language(message)
            DB.inc_reg_step(chat_id)

        elif DB.get_reg_step(chat_id) == CHOOSING_THEME:
            set_theme(message)
            DB.inc_reg_step(chat_id)

        else:
            bot.send_message(chat_id, "ERROR")
    else:
        bot.send_message(chat_id, "Send /start first!")


bot.polling()
