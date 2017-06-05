import telebot
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['/start', '/help'])
def send_welcome(message):
    bot.reply_to(message, "Fuck off!")


@bot.message_handler(func=lambda m: True)
def echo_mesage(message):
    bot.send_message(message.chat.id, "Fuck off!")


bot.polling()
