import telebot
import time
import pymysql.cursors
from telebot import types

print('@ElfochkaBirthdayReminderBot запущен')

# Connect to the database


# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `BirthdayReminderBot` (`user_id`, `birthday_name`) VALUES (%s, %s)"
#         cursor.execute(sql, ('1111', 'very-secret'))
#
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
#
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `user_id`, `birthday_name` FROM `BirthdayReminderBot` WHERE `user_id`=%s"
#         cursor.execute(sql, ('1111',))
#         result = cursor.fetchone()
#         print(result)


bot = telebot.TeleBot("5464014913:AAEW7TYzUvNurSjsIT4xwuwf7KOKogmODIQ")  # токен бота

new_birthday_name = ''
new_birthday_date = ''
new_remind_or_not = False
new_reminder_period = 0


@bot.message_handler(content_types=['text'])
def start(message=''):
    # if message.text == '/start':
    #     my_text = ('@ElfochkaBirthdayReminderBot запущен' + '\nПользователь: @' + str(
    #         message.from_user.username) + '\nПользователь: ' + str(message.from_user.id))
    #     bot.send_message(my_group_id, my_text,timeout=1000)

    if message.text == '/add':
        bot.send_message(message.from_user.id, 'Напиши имя именника')
        bot.register_next_step_handler(message, birthday_name)  # следующий шаг – функция birthday_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /add для добавления новой записи')


def birthday_name(message):
    global new_birthday_name
    if message.text != '':
        new_birthday_name = message.text
        bot.send_message(message.from_user.id, 'Напиши день и месяц рождения в формате ДД.ММ. Например: 27.03')
        bot.register_next_step_handler(message, birthday_date)  # следующий шаг – функция birthday_date
    else:
        bot.send_message(message.from_user.id, 'Имя именника незаполненно, давай сначала')
        start(message)


def birthday_date(message):
    global new_birthday_date
    if message.text != '' and len(message.text) == 5 and str(message.text)[2] == '.':
        if str(message.text).split('.')[0].isdigit() and str(message.text).split('.')[1].isdigit():
            new_birthday_date = message.text
            # bot.send_message(message.from_user.id, 'Нужно ли напомнить о дате заранее? Да/Нет')
            # bot.register_next_step_handler(message, remind_or_not)  # следующий шаг – функция remind_or_not
        else:
            bot.send_message(message.from_user.id, 'Дата введена некорректно')
            bot.send_message(message.from_user.id,
                             'Дата введена некорректно\nНапиши день и месяц рождения в формате ДД.ММ. Например: 27.03')
            birthday_date(message)

    # def remind_or_not(message):
    #     global new_remind_or_not
    #     if str(message.text).lower() == 'Да':
    #         new_remind_or_not = True
    #     bot.send_message(message.from_user.id, 'За сколько дней напомнить?')
    #     bot.register_next_step_handler(message, reminder_period)  # следующий шаг – функция birthday_date
    #
    #
    # def reminder_period(message):
    #     global new_reminder_period
    #     if int(message.text) > 0:
    #         new_reminder_period = int(message.text)
    #     else:

    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);

    question = '👤: ' + new_birthday_name + '\n📆: ' + new_birthday_date

    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки

        connection = pymysql.connect(host='31.31.198.35',
                                     user='u1771772_default',
                                     password='56f6hDDRxt96FSvu',
                                     database='u1771772_default',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                sql = "INSERT INTO `BirthdayReminderBot` (`user_id`, `birthday_name`, `birthday_date`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (
                    call.message.chat.id, new_birthday_name, new_birthday_date))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        bot.send_message(call.message.chat.id, 'Я всё запомнил');
    elif call.data == "no":
        bot.send_message(call.from_user.id, 'Тогда давай сначала')
        start()


# new_birthday_name = ''
# new_birthday_date = ''
# new_remind_or_not = False
# new_reminder_period = 0

# user_id +
# birthday_name +
# birthday_user_name -
# birthday_date +
# remind_or_not +
# reminder_period +
# chat_id
# text
# group_id
# user_name

# def get_new_record(message):
#     new_name = str(message.text).split('/')[0]
#     new_date = str(message.text).split('/')[1]
#
#     new_record = bot.send_message(message.from_user.id, ('👤: ' + new_name + '\n📆: ' + new_date))
#     new_record_id = new_record.id
#     new_record_text = new_record.text
#
#     print(new_record_id)
#     print(new_record_text)


if __name__ == '__main__':
    while True:
        try:  # добавляем try для бесперебойной работы
            bot.polling(none_stop=True)  # запуск бота
        except:
            time.sleep(10)  # в случае падения
