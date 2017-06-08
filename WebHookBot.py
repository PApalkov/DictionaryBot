import cherrypy
import telebot
from config import token
import DBconnector as DB
import support
from support import ENGLISH_LANGUAGE, RUSSIAN_LANGUAGE, FRENCH_LANGUAGE, GERMAN_LANGUAGE
from Translator import translate


#================== START OF WEBHOOK PART==============

WEBHOOK_HOST = '95.85.10.122'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token

bot = telebot.TeleBot(token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)




#Registration Steps
CHOOSING_FIRST_LANGUAGE = 0
CHOOSING_SECOND_LANGUAGE = 1
CHOOSING_THEME = 2
FINISHED = 3


COMMON_THEME = "COMMON"
TECH_THEME = "TECH"
MED_THEME = "MEDICINE"
LEGAL_THEME = "LEGAL"


@bot.message_handler(commands=['start'])
def start_message(message):

    intro_message = support.get_intro_message()

    chat_id = message.chat.id
    if not(DB.contains_person(chat_id)):

        name = message.chat.first_name
        last_name = message.chat.last_name
        registration_step = CHOOSING_FIRST_LANGUAGE
        DB.insert_person(chat_id, name, last_name, registration_step)

        lang_keyboard = support.make_language_keyboard()

        bot.send_message(chat_id, intro_message)
        bot.send_message(chat_id, text="Choose your language:", reply_markup=lang_keyboard)

    else:
        send_words(message)


@bot.message_handler(commands=['stop'])
def last_message(message):
    del_keyboard = telebot.types.ReplyKeyboardRemove()
    DB.del_person(message.chat.id)
    text = "See you later!"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=del_keyboard)


def send_words(message):
    chat_id = message.chat.id

    first_language = DB.get_first_language(chat_id)
    second_language = DB.get_second_language(chat_id)

    if message.text == "GET WORDS":

        progress = DB.get_progress(chat_id)
        theme = DB.get_theme(chat_id)
        words = DB.select_from_dictionary(second_language, progress, 10, theme)

        translated_words = ""

        if len(words) > 0:
            for word in words:
                translation = translate(word, second_language, first_language)

                #if the word is rubbish
                if not(word == translation):
                    translated_words += word + " - " + translation + "\n"

            DB.inc_progress(chat_id)

            bot.send_message(chat_id, translated_words)
        else:
            bot.send_message(chat_id, "You have finished this part!")
    else:
        #translating the word from person
        word = message.text
        translation = translate(word, second_language, first_language)
        bot.send_message(chat_id, translation)



def set_first_language(message):
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

    elif theme == TECH_THEME:
        DB.set_theme(chat_id, TECH_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)

    elif theme == MED_THEME:
        DB.set_theme(chat_id, MED_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)

    elif theme == LEGAL_THEME:
        DB.set_theme(chat_id, LEGAL_THEME)
        bot.send_message(chat_id=chat_id, text="Enjoy!",
                         reply_markup=send_words_keyboard)

    else:
        theme_keyboard = support.make_theme_keyboard()
        bot.send_message(chat_id=chat_id, text="Choose the theme:",
                         reply_markup=theme_keyboard)


@bot.message_handler(func=lambda m: True, content_types=['text'])
def usual_messages(message):
    chat_id = message.chat.id



    if DB.contains_person(chat_id):

        if DB.get_reg_step(chat_id) == FINISHED:
            send_words(message)


        elif DB.get_reg_step(chat_id) == CHOOSING_FIRST_LANGUAGE:

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



bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})