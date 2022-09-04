import telebot
import time
import pymysql.cursors
from telebot import types


print('@BirthdayReminderBot запущен')

# connection = pymysql.connect(host='31.31.198.35',
#                              user='u1771772_default',
#                              password='56f6hDDRxt96FSvu',
#                              database='u1771772_default',
#                              cursorclass=pymysql.cursors.DictCursor)
# print('connection - Done')

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


@bot.message_handler(content_types=['text'])
def start(message):
    print('Start - Start')
    global new_user_name, user_id
    new_user_name = message.from_user.username

    if message.text == '/add':
        bot.send_message(message.from_user.id, 'Добавь запись: Имя именника/дата рождения ДД.ММ')
        bot.register_next_step_handler(message, add_new_entry)  # следующий шаг – функция add_new_entry
    elif message.text == '/list':
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, 'Все твои записи:')
        print('/list - Done')
        print(user_id)

        # bot.register_next_step_handler(message, user_list)  # следующий шаг – функция user_list
        user_list()
    else:
        bot.send_message(message.from_user.id, help_message)

    print('Start - Done')


def add_new_entry(message):
    print('add_new_entry - Start')
    global new_birthday_name, new_birthday_date, new_remind_or_not, new_reminder_period, new_user_name
    try:
        new_entry = str(message.text).split('/')
        new_birthday_name = new_entry[0]
        new_birthday_date = new_entry[1]

        print('add_new_entry - Processing')
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Записать', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Отмена', callback_data='no');
        keyboard.add(key_no);
        print('keyboard - Done')
        question = '👤: ' + new_birthday_name + '\n📆: ' + new_birthday_date

        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        # bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    except:
        bot.send_message(message.from_user.id, error_message)
        bot.register_next_step_handler(message, start)  # следующий шаг – функция start

    print('add_new_entry - Done')


def user_list():
    connection_list = pymysql.connect(host='31.31.198.35',
                                      user='u1771772_default',
                                      password='56f6hDDRxt96FSvu',
                                      database='u1771772_default',
                                      cursorclass=pymysql.cursors.DictCursor)

    print('user_list - Start')
    # user_id = message.from_user.id
    #
    global connection, user_id
    # user_id = user_idd
    try:
        with connection_list:
            print('user_list - connection - Start')
            print(user_id)

            with connection_list.cursor() as cursor_list:
                sql_list = "SELECT * FROM `BirthdayReminderBot` WHERE `user_id`=%s"
                cursor_list.execute(sql_list, (str(user_id),))
                result = cursor_list.fetchall()
                for line in result:
                    print('user_list - connection - Done')
                    # print(str(line['id']))
                    print(str(line['birthday_name']))
                    print(str(line[
                                  'birthday_date']))
                    # '🆔: `' + line['id'] + '`' + '\n' +
                    list_line = '🆔: `' + str(line['id']) + '`\n' + '👤: *' + str(
                        line['birthday_name']) + '*\n📆: ' + str(line[
                                                                     'birthday_date'])

                    print('user_list - list_line - Done')

                    bot.send_message(user_id, list_line, parse_mode='MarkDown')
            # connection.commit()
        print('user_list - Done')
    except:
        bot.send_message(user_id, error_message)

    # finally:
    #     connection.close()


def remind_congratulate():
    connection_remind_congratulate = pymysql.connect(host='31.31.198.35',
                                                     user='u1771772_default',
                                                     password='56f6hDDRxt96FSvu',
                                                     database='u1771772_default',
                                                     cursorclass=pymysql.cursors.DictCursor)

    now_date = time.strftime('%d.%m', time.localtime())

    print('remind_congratulate - connection_remind_congratulate - Done')
    with connection_remind_congratulate:
        with connection_remind_congratulate.cursor() as cursor_remind_congratulate:
            sql = "SELECT * FROM `BirthdayReminderBot` WHERE `birthday_date`=%s"
            cursor_remind_congratulate.execute(sql, (str(now_date),))
            result = cursor_remind_congratulate.fetchall()
            print(result)
            print('remind_congratulate - result - Done')

            for line in result:

                # now_date = time.strftime('%d.%m', time.localtime())

                print('remind_congratulate - ' + now_date + ' - Done')

                # if line['birthday_date'] == now_date:
                congratulate_text = 'Сегодня ' + line['birthday_date'] + ' отмечает свой День Рождения *' + line[
                    'birthday_name'] + '*'

                bot.send_message(line['user_id'], congratulate_text, parse_mode='MarkDown')

    print('remind_congratulate - Done')
    time.sleep(100)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    connection_add = pymysql.connect(host='31.31.198.35',
                                     user='u1771772_default',
                                     password='56f6hDDRxt96FSvu',
                                     database='u1771772_default',
                                     cursorclass=pymysql.cursors.DictCursor)

    print('callback_worker - Start')
    global new_birthday_name, new_birthday_date, new_user_name
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':

            with connection_add:
                print('connection - Done')
                with connection_add.cursor() as cursor_add:
                    print('connection.cursor() - Done')
                    print(call.message.chat.id)
                    print(new_birthday_name)
                    print(new_birthday_date)
                    print('@' + new_user_name)
                    print('Add all - Done')
                    sql_add = "INSERT INTO `BirthdayReminderBot` (`user_id`, `birthday_name`, `birthday_date`, `user_name`) VALUES (%s, %s, %s, %s)"
                    cursor_add.execute(sql_add, (
                        call.message.chat.id, new_birthday_name, new_birthday_date,
                        ('@' + new_user_name)))
                    print('cursor_add.execute - Done')
                connection_add.commit()
                print('connection.commit() - Done')
            # connection.close()
            # print('connection.close() - Done')
            new_user_name, new_birthday_name, new_birthday_date = '', '', ''

            bot.send_message(call.message.chat.id, 'Я всё запомнил!')



        else:
            new_user_name, new_birthday_name, new_birthday_date = '', '', ''
            bot.send_message(call.message.chat.id, error_message)

    elif call.data == "no":
        if new_user_name != '' or new_birthday_name != '' or new_birthday_date != '':
            bot.send_message(call.message.chat.id, 'Отменил.')
            bot.send_message(call.message.chat.id, help_message)

    print('callback_worker - Done')


# schedule.every().day.at("14:30").do(remind_congratulate)
# scheduler.add_job(remind_congratulate, "interval", seconds=35)

if __name__ == '__main__':

    while True:
        try:  # добавляем try для бесперебойной работы
            # current_time = time.strftime('%H:%M', time.localtime())
            # remind_times = ['11:00', '15:00', '19:00', '14:57']
            # if current_time in remind_times:
            #     print('remind_congratulate() - Start')
            #     remind_congratulate()

            bot.polling(none_stop=True)  # запуск бота
            # schedule.run_pending()
            # time.sleep(1)

        except:
            print('time.sleep(1) - Done')

            time.sleep(15)  # в случае падения
