import telebot
import time
import pymysql.cursors
from telebot import types
import schedule

print('@BirthdayReminderBot запущен')

connection = pymysql.connect(host='31.31.198.35',
                             user='u1771772_default',
                             password='56f6hDDRxt96FSvu',
                             database='u1771772_default',
                             cursorclass=pymysql.cursors.DictCursor)

bot = telebot.TeleBot("5464014913:AAEW7TYzUvNurSjsIT4xwuwf7KOKogmODIQ")  # токен бота

new_entry_id = ''
new_birthday_name = ''
new_birthday_date = ''
new_remind_or_not = False
new_reminder_period = 0
new_user_name = ''
user_id = ''

hello_message = 'Привет! Я - Бот напоминалка о днях рождения!'
help_message = 'Введи /add для добавления новой записи\n' \
               'Введи /list для просмотра всех твоих записей'

error_message = 'Что-то пошло не так. Давай сначала.'


# def remind_congratulate():
#     print('test 1')
#     global connection
#     print('test 2')
#     with connection:
#         with connection.cursor() as cur:
#             sql = "SELECT * FROM `BirthdayReminderBot`"
#             cur.execute(sql, (user_id,))
#             result = cur.fetchall()
#             for line in result:
#
#                 now_date = time.strftime('%d.%m', time.localtime())
#
#                 # print(now_date)
#
#                 if line['birthday_date'] == now_date:
#                     congratulate_text = 'Сегодня ' + line['birthday_date'] + 'отмечает свой День Рождения ' + line[
#                         'birthday_name']
#
#                     bot.send_message(line['user_id'], congratulate_text)


@bot.message_handler(content_types=['text'])
def start(message):
    global new_user_name, user_id
    new_user_name = message.from_user.username

    if message.text == '/add':
        bot.send_message(message.from_user.id, 'Добавь запись: Имя именника/дата рождения ДД.ММ')
        bot.register_next_step_handler(message, add_new_entry)  # следующий шаг – функция add_new_entry
    elif message.text == '/list':
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, 'Все твои записи:')
        # bot.register_next_step_handler(user_id, user_list)  # следующий шаг – функция user_list
        user_list(user_id)
    else:
        bot.send_message(message.from_user.id, help_message)


def add_new_entry(message):
    global new_entry_id, new_birthday_name, new_birthday_date, new_remind_or_not, new_reminder_period, new_user_name
    try:
        new_entry = str(message.text).split('/')
        new_birthday_name = new_entry[0]
        new_birthday_date = new_entry[1]

        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Записать', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Отмена', callback_data='no');
        keyboard.add(key_no);

        question = '👤: ' + new_birthday_name + '\n📆: ' + new_birthday_date

        new_entry_id = bot.send_message(message.from_user.id, text=question, reply_markup=keyboard).id


    except:
        bot.send_message(message.from_user.id, error_message)
        bot.register_next_step_handler(message, start)  # следующий шаг – функция start


def user_list(user_idd):
    global connection, user_id
    user_id = user_idd
    try:
        with connection:
            with connection.cursor() as cur:
                sql = "SELECT * FROM `BirthdayReminderBot` WHERE `user_id`=%s"
                cur.execute(sql, (user_id,))
                result = cur.fetchall()
                # print(result)
                for line in result:
                    # print(line)
                    # print(type(line))
                    # print(line['birthday_name'])
                    # for key, value in line.items:
                    #     print(value)
                    # print('тест' + result)

                    list_line = '🆔: `' + line['id'] + '`' + '\n' + '👤: ' + line['birthday_name'] + '\n📆: ' + line[
                        'birthday_date']

                    bot.send_message(user_id, list_line, parse_mode='MarkDown')
    except:
        bot.send_message(user_id, error_message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global new_entry_id, new_birthday_name, new_birthday_date, new_user_name, connection
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':

            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `BirthdayReminderBot` (`id`, `user_id`, `birthday_name`, `birthday_date`, `user_name`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                        new_entry_id, call.message.chat.id, new_birthday_name, new_birthday_date,
                        ('@' + new_user_name)))
                connection.commit()

            new_user_name, new_birthday_name, new_birthday_date = '', '', ''

            bot.send_message(call.message.chat.id, 'Я всё запомнил!')

        else:
            new_user_name, new_birthday_name, new_birthday_date = '', '', ''
            bot.send_message(call.message.chat.id, error_message)

    elif call.data == "no":
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':
            bot.send_message(call.message.chat.id, 'Отменил.')
            bot.send_message(call.message.chat.id, help_message)


# schedule.every().day.at("00:15").do(remind_congratulate)


if __name__ == '__main__':

    while True:
        try:  # добавляем try для бесперебойной работы
            bot.polling(none_stop=True)  # запуск бота
            # current_time = time.strftime('%H:%M', time.localtime())
            # if current_time == '00:40':
            #     remind_congratulate()
        except:
            time.sleep(10)  # в случае падения

