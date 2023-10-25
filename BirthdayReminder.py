import telebot
import time
import pymysql.cursors
from telebot import types
import datetime
import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
MY_ID = os.getenv('MY_ID')

# bot = telebot.TeleBot("5407469548:AAHpPNs0W8_4DWOUP3gNm1wtIkKnACxp9iY")
# Тестовый БОТ Super Bot
bot = telebot.TeleBot(BOT_TOKEN)
# Рабочий BirthdayReminderBot

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
    if message.from_user.username:
        new_user_name = message.from_user.username
    user_id = message.from_user.id

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'start - Start')

    if message.text == '/add':
        bot.send_message(message.from_user.id, 'Добавь запись: Имя именника/дата рождения ДД.ММ')
        # my_log(str(user_id) + ': @' + str(new_user_name) + ':' + '/add - Done')
        bot.register_next_step_handler(message, add_new_entry)  # следующий шаг – функция add_new_entry
    elif message.text == '/list':
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, 'Список твоих записей:')
        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + '/list - Done')
        user_list(str(user_id))
    elif message.text == '/del':
        bot.send_message(message.from_user.id, 'Скопируй из спика и пришли номер id записи, которую нужно удалить.')
        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + '/del - Start')
        bot.register_next_step_handler(message, del_entry)  # следующий шаг – функция del_entry
    elif message.text == '/edit':
        bot.send_message(message.from_user.id, 'Для отправки поздравления в чат скопируй из спика и пришли номер id '
                                               'записи и id чата. В формате id_записи/idчата1, idчата2, idчата3\n'
                                               'Например: 0001/-2000000001')
        bot.send_message(message.from_user.id, 'если вы не знаете id чата воспользуйтесь командой /getid')
        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + '/edit - Start')
        bot.register_next_step_handler(message, edit_entry)  # следующий шаг – функция edit_entry
    elif message.text == '/getid':
        bot.send_message(message.from_user.id, 'Перешли сообщение юзера или чата, ID которого хочешь узнать'
                                               '(Если ты хочешь узнать ID чата, то пересылай именно сообщения чата, '
                                               'не людей, которые пишут в этом чате')
        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + '/getid - Start')

        bot.register_next_step_handler(message, get_chat_id)  # следующий шаг – функция get_chat_id

    else:
        bot.send_message(message.from_user.id, help_message)

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'start - Done')


# добавление новой записи
def add_new_entry(message):
    global new_birthday_name, new_birthday_date, new_remind_or_not, new_reminder_period, new_user_name

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - Start')

    try:
        if '/' not in str(message.text):
            bot.send_message(message.from_user.id, 'Не хватает разделителя "/" между именем и датой')
            raise ZeroDivisionError

        new_entry = str(message.text).split('/')
        new_birthday_name = new_entry[0]
        new_birthday_date = new_entry[1]

        if new_birthday_name == '':
            if new_birthday_date.isalpha():
                raise IndexError
            else:
                bot.send_message(message.from_user.id, 'Имя не может быть пустым')
                raise ZeroDivisionError
        elif '.' not in new_birthday_date:
            bot.send_message(message.from_user.id, 'Формат даты должен быть записан через точку, сначала день, '
                                                   'затем месяц. Например "31.12" - 31е Декабря')
            raise ZeroDivisionError

        ddmm = str(new_birthday_date).split('.')
        dd = ddmm[0]
        mm = ddmm[1]

        if len(dd) != 2 or len(mm) != 2:
            bot.send_message(message.from_user.id, 'Дата должна иметь вид "ДД.ММ" в днях и месяце по две цифры, '
                                                   'например: "03.03" (3е марта)')
            raise ZeroDivisionError

        elif int(dd) > 31 or int(mm) > 12:
            bot.send_message(message.from_user.id,
                             'Проверьте дату. Дней должно быть не больше 31, а месяц не больше 12')
            raise ZeroDivisionError

        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - Processing')

        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Записать', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Отмена', callback_data='no');
        keyboard.add(key_no);

        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'keyboard - Done')

        question = '👤: ' + new_birthday_name + '\n📆: ' + new_birthday_date

        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    except ZeroDivisionError:
        bot.send_message(message.from_user.id, 'Попробуй еще Имя именника/дата рождения ДД.ММ')
        bot.register_next_step_handler(message, add_new_entry)  # следующий шаг – функция add_new_entry

    except:
        bot.send_message(message.from_user.id, error_message)
        bot.send_message(message.from_user.id, help_message)

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'add_new_entry - PreDone')


# Список дней рождений юзера
def user_list(list_user_id):
    connection_list = pymysql.connect(host=HOST,
                                      user=USER,
                                      password=PASSWORD,
                                      database=DATABASE,
                                      cursorclass=pymysql.cursors.DictCursor)

    global user_id, new_user_name
    user_id = list_user_id
    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'user_list - Start')

    try:
        with connection_list:

            with connection_list.cursor() as cursor_list:
                sql_list = "SELECT * FROM `BirthdayReminderBot` WHERE `user_id`=%s"
                cursor_list.execute(sql_list, (str(user_id),))
                result = cursor_list.fetchall()

                for line in result:

                    chat_id_text = ''

                    if str(line['chat_id']) != '':
                        chat_id_text = '\n💬: ' + str(line['chat_id'])

                    list_line = '🆔: `' + str(line['id']) + '`\n' + '👤: *' + str(
                        line['birthday_name']) + '*\n📆: ' + str(line['birthday_date']) + str(chat_id_text)

                    bot.send_message(user_id, list_line, parse_mode='MarkDown')
        bot.send_message(user_id, 'Для удаления записи введите /del\n'
                                  'Для изменения записи введите /edit')

    except:
        bot.send_message(user_id, error_message)

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'user_list - Done')


# обработка напоминания о сегодняшнем или предстоящем ДР
def remind_congratulate():
    # my_log('remind_congratulate - Start')
    connection_remind_congratulate = pymysql.connect(host=HOST,
                                                     user=USER,
                                                     password=PASSWORD,
                                                     database=DATABASE,
                                                     cursorclass=pymysql.cursors.DictCursor)

    now_date = time.strftime('%d.%m', time.localtime())
    bot.send_message(MY_ID, 'Проверка связи {}'.format(now_date), parse_mode='MarkDown')

    with connection_remind_congratulate:
        with connection_remind_congratulate.cursor() as cursor_remind_congratulate:
            sql = "SELECT * FROM `BirthdayReminderBot` WHERE `birthday_date`=%s"
            cursor_remind_congratulate.execute(sql, (str(now_date),))
            result = cursor_remind_congratulate.fetchall()
            # print('Done1')
            # my_log('remind_congratulate - result - Done')
            for line in result:
                # my_log('remind_congratulate - ' + now_date + ' - Done')
                # print('Done2')
                try:
                    # today_date = 'Сегодня '

                    today_date = 'Сегодня ' + line['birthday_date'] + ' отмечает свой День Рождения *' + line[
                        'birthday_name'] + '*'

                    # print('Done3.1')
                    congratulate_text = '*' + line['birthday_name'] + '*, с днём Рождения!'
                    # print('Done3.2')
                    bot.send_message(line['user_id'], today_date, parse_mode='MarkDown')
                    # print('Done3.3')
                    if line['chat_id'] != '0' or line['chat_id'] != '':
                        # print('re')
                        for chat_id in str(line['chat_id']).split(', '):
                            # print(int(chat_id))
                            bot.send_message(int(chat_id), congratulate_text, parse_mode='MarkDown')
                except:
                    pass

        remind_period = [1, 3, 7]

        for i in remind_period:
            date_reminder = datetime.datetime.today() + datetime.timedelta(days=i)
            date_reminder = date_reminder.strftime('%d.%m')

            with connection_remind_congratulate.cursor() as cursor_remind_before:
                sql = "SELECT * FROM `BirthdayReminderBot` WHERE `birthday_date`=%s"
                cursor_remind_before.execute(sql, (str(date_reminder),))
                result = cursor_remind_before.fetchall()

                # my_log('cursor_remind_before - result - Done')
                for line in result:
                    # my_log('cursor_remind_before - ' + now_date + ' - Done')

                    congratulate_text = 'Не забудь, ' + line['birthday_date'] + ' отмечает свой День Рождения *' + line[
                        'birthday_name'] + '*'

                    bot.send_message(line['user_id'], congratulate_text, parse_mode='MarkDown')

    time.sleep(100)


# удаление записи по id
def del_entry(message):
    global user_id, new_user_name

    user_id = message.from_user.id

    connection_del_entry = pymysql.connect(host=HOST,
                                           user=USER,
                                           password=PASSWORD,
                                           database=DATABASE,
                                           cursorclass=pymysql.cursors.DictCursor)
    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'del_entry - connection - Done')

    try:

        if '/' in str(message.text) and str(message.text).split('/')[1].isalpha():
            raise BaseException

        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'del_entry - connection - try')

        with connection_del_entry:

            # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'del_entry - connection - connection_del_entry')

            with connection_del_entry.cursor() as cursor_del_entry:
                # my_log(
                #     str(user_id) + ': @' + str(
                #         new_user_name) + ': ' + 'del_entry - connection - '
                #                                 'with connection_del_entry.cursor() as cursor_del_entry' + message.text)

                sql_del = "DELETE FROM `BirthdayReminderBot` WHERE `id`=%s AND `user_id`=%s"
                cursor_del_entry.execute(sql_del, (message.text, user_id))

                # my_log(str(user_id) + ': @' + str(
                #     new_user_name) + ': ' + 'del_entry - cursor_del_entry - Done ' + str(message.text) + ' : ' + str(
                #     message.from_user.id))

            connection_del_entry.commit()

            # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'del_entry - Done')
            bot.send_message(message.from_user.id, 'Удалил запись')

            user_list(str(user_id))

    except:
        bot.send_message(user_id, error_message)
        bot.send_message(user_id, help_message)


# редактирование записи по id
def edit_entry(message):
    global user_id, new_user_name

    user_id = message.from_user.id
    message_text = str(message.text).split('/')

    connection_edit_entry = pymysql.connect(host=HOST,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DATABASE,
                                            cursorclass=pymysql.cursors.DictCursor)
    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'edit_entry - connection - Done')

    try:

        if '/' in str(message.text) and str(message.text).split('/')[1].isalpha():
            raise BaseException

        # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'edit_entry - connection - try')

        with connection_edit_entry:

            # my_log(
            #     str(user_id) + ': @' + str(new_user_name) + ': ' + 'edit_entry - connection - connection_edit_entry')

            with connection_edit_entry.cursor() as cursor_edit_entry:
                # my_log(
                #     str(user_id) + ': @' + str(
                #         new_user_name) + ': ' + 'edit_entry - connection - '
                #                                 'with connection_edit_entry.cursor() as cursor_edit_entry' + message.text)

                sql_edit = "UPDATE `BirthdayReminderBot` SET `chat_id` = %s WHERE `id` = %s"
                cursor_edit_entry.execute(sql_edit, (message_text[1], message_text[0]))

            connection_edit_entry.commit()

            # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'edit_entry - Done')
            bot.send_message(message.from_user.id, 'Скорректировал запись')

            user_list(str(user_id))

    except:
        bot.send_message(user_id, error_message)
        bot.send_message(user_id, help_message)


def get_chat_id(message):
    print(message)
    get_chat_id_message = 'Ваш id: `' + str(message.from_user.id) + '`\nПереслано от *' + str(
        message.forward_from_chat.title) + '*, id: `' + str(
        message.forward_from_chat.id) + '`'

    bot.send_message(message.from_user.id, get_chat_id_message, parse_mode='MarkDown')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    connection_add = pymysql.connect(host=HOST,
                                     user=USER,
                                     password=PASSWORD,
                                     database=DATABASE,
                                     cursorclass=pymysql.cursors.DictCursor)

    global new_birthday_name, new_birthday_date, new_user_name, user_id

    # if new_user_name == '':
    #     new_user_name = ''
    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'callback_worker - Start')

    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':

            with connection_add:
                with connection_add.cursor() as cursor_add:
                    sql_add = "INSERT INTO `BirthdayReminderBot` (`user_id`, `birthday_name`, `birthday_date`, `user_name`) VALUES (%s, %s, %s, %s)"
                    cursor_add.execute(sql_add, (
                        call.message.chat.id, new_birthday_name, new_birthday_date,
                        ('@' + new_user_name)))

                    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'cursor_add.execute - Done')

                connection_add.commit()

                # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'connection.commit() - Done')

            new_user_name, new_birthday_name, new_birthday_date = '', '', ''

            bot.send_message(call.message.chat.id, 'Я всё запомнил!')

        else:
            new_user_name, new_birthday_name, new_birthday_date = '', '', ''
            bot.send_message(call.message.chat.id, error_message)

    elif call.data == "no":
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':
            bot.send_message(call.message.chat.id, 'Отменил.')
            bot.send_message(call.message.chat.id, help_message)

    # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'callback_worker - Done')


if __name__ == '__main__':

    while True:
        try:  # добавляем try для бесперебойной работы
            bot.polling(none_stop=True)  # запуск бота
        except:
            # my_log(str(user_id) + ': @' + str(new_user_name) + ': ' + 'Global except time.sleep(15) - Done')
            time.sleep(15)  # в случае падения
