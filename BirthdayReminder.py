import telebot
import time
import pymysql.cursors
from telebot import types

print('@BirthdayReminderBot запущен')

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

print('TeleBot - Done')


def my_log(log_text):
    try:
        with open('BirthdayReminderLog.txt', 'a') as file_log:
            time_stamp_now = time.strftime('%d.%m.%y %H:%M:%S', time.localtime())
            file_log.write(str(time_stamp_now) + ' : ' + log_text + '\n')

    except:
        pass


@bot.message_handler(content_types=['text'])
def start(message):
    global new_user_name, user_id
    new_user_name = message.from_user.username
    user_id = message.from_user.id

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'start - Start')

    if message.text == '/add':
        bot.send_message(message.from_user.id, 'Добавь запись: Имя именника/дата рождения ДД.ММ')
        my_log(str(user_id) + ': @' + str(new_user_name) + ':' + '/add - Done')
        bot.register_next_step_handler(message, add_new_entry)  # следующий шаг – функция add_new_entry
    elif message.text == '/list':
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, 'Все твои записи:')
        my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + '/list - Done')

        user_list()

    else:
        bot.send_message(message.from_user.id, help_message)

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'start - Done')


def add_new_entry(message):
    global new_birthday_name, new_birthday_date, new_remind_or_not, new_reminder_period, new_user_name

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - Start')

    try:
        new_entry = str(message.text).split('/')
        new_birthday_name = new_entry[0]
        new_birthday_date = new_entry[1]

        # if new_birthday_name == '':
        # bot.send_message(message.from_user.id, 'Имя не заполнено')
        # bot.register_next_step_handler(message, start)  # следующий шаг – функция start

        my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - Processing')

        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Записать', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Отмена', callback_data='no');
        keyboard.add(key_no);

        my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'keyboard - Done')

        question = '👤: ' + new_birthday_name + '\n📆: ' + new_birthday_date

        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    except:
        bot.send_message(message.from_user.id, error_message)
        bot.register_next_step_handler(message, start)  # следующий шаг – функция start

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - PreDone')


def user_list():
    connection_list = pymysql.connect(host='31.31.198.35',
                                      user='u1771772_default',
                                      password='56f6hDDRxt96FSvu',
                                      database='u1771772_default',
                                      cursorclass=pymysql.cursors.DictCursor)

    global user_id, new_user_name

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'user_list - Start')

    try:
        with connection_list:

            with connection_list.cursor() as cursor_list:
                sql_list = "SELECT * FROM `BirthdayReminderBot` WHERE `user_id`=%s"
                cursor_list.execute(sql_list, (str(user_id),))
                result = cursor_list.fetchall()

                for line in result:
                    list_line = '🆔: `' + str(line['id']) + '`\n' + '👤: *' + str(
                        line['birthday_name']) + '*\n📆: ' + str(line[
                                                                     'birthday_date'])
                    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'user_list - list_line id# ' + str(
                    #     line['id']) + ' - Done')

                    bot.send_message(user_id, list_line, parse_mode='MarkDown')


    except:
        bot.send_message(user_id, error_message)

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'user_list - Done')


def remind_congratulate():
    connection_remind_congratulate = pymysql.connect(host='31.31.198.35',
                                                     user='u1771772_default',
                                                     password='56f6hDDRxt96FSvu',
                                                     database='u1771772_default',
                                                     cursorclass=pymysql.cursors.DictCursor)

    now_date = time.strftime('%d.%m', time.localtime())

    global user_id, new_user_name

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'remind_congratulate - connection - Done')

    with connection_remind_congratulate:
        with connection_remind_congratulate.cursor() as cursor_remind_congratulate:
            sql = "SELECT * FROM `BirthdayReminderBot` WHERE `birthday_date`=%s"
            cursor_remind_congratulate.execute(sql, (str(now_date),))
            result = cursor_remind_congratulate.fetchall()

            my_log(str(user_id) + ': @' + str(
                new_user_name) + ':' + 'remind_congratulate - result - Done' + result)

            for line in result:
                my_log(
                    str(user_id) + ': @' + str(new_user_name) + ': ' + 'remind_congratulate - ' + now_date + ' - Done')

                congratulate_text = 'Сегодня ' + line['birthday_date'] + ' отмечает свой День Рождения *' + line[
                    'birthday_name'] + '*'

                bot.send_message(line['user_id'], congratulate_text, parse_mode='MarkDown')

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'remind_congratulate - Done')

    time.sleep(100)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    connection_add = pymysql.connect(host='31.31.198.35',
                                     user='u1771772_default',
                                     password='56f6hDDRxt96FSvu',
                                     database='u1771772_default',
                                     cursorclass=pymysql.cursors.DictCursor)

    global new_birthday_name, new_birthday_date, new_user_name, user_id

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'callback_worker - Start')

    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':

            with connection_add:
                with connection_add.cursor() as cursor_add:
                    sql_add = "INSERT INTO `BirthdayReminderBot` (`user_id`, `birthday_name`, `birthday_date`, `user_name`) VALUES (%s, %s, %s, %s)"
                    cursor_add.execute(sql_add, (
                        call.message.chat.id, new_birthday_name, new_birthday_date,
                        ('@' + new_user_name)))

                    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'cursor_add.execute - Done')

                connection_add.commit()

                my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'connection.commit() - Done')

            new_user_name, new_birthday_name, new_birthday_date = '', '', ''

            bot.send_message(call.message.chat.id, 'Я всё запомнил!')



        else:
            new_user_name, new_birthday_name, new_birthday_date = '', '', ''
            bot.send_message(call.message.chat.id, error_message)

    elif call.data == "no":
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':
            bot.send_message(call.message.chat.id, 'Отменил.')
            bot.send_message(call.message.chat.id, help_message)

    my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'callback_worker - Done')


if __name__ == '__main__':

    while True:
        try:  # добавляем try для бесперебойной работы
            bot.polling(none_stop=True)  # запуск бота
        except:
            my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'Global except time.sleep(15) - Done')
            time.sleep(15)  # в случае падения
