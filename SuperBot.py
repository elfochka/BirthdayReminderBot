from subprocess import check_output
from subprocess import check_call

import telebot
import time

print('SupeBot запущен')

bot = telebot.TeleBot("5407469548:AAH66oGKqUE5PWm-dOGCixXk0sZWRMlyglE")  # токен бота
user_id = 142351451  # id вашего аккаунта


@bot.message_handler(content_types=["text"])
def main(message):
    if (user_id == message.chat.id):  # проверяем, что пишет именно владелец
        comand = message.text[1:]  # текст сообщения

        # bot.send_message(message.chat.id, comand)

        try:  # если команда невыполняемая - check_output выдаст exception
            bot.send_message(message.chat.id, check_output(comand, shell=True))
        except:
            bot.send_message(message.chat.id, "Invalid input")  # если команда некорректна


if __name__ == '__main__':
    while True:
        try:  # добавляем try для бесперебойной работы
            bot.polling(none_stop=True)  # запуск бота
        except:
            time.sleep(10)  # в случае падения
