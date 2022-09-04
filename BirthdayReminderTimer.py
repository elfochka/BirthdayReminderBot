import time
from BirthdayReminder import remind_congratulate

# import BirthdayReminder

print('BirthdayReminderTimer запущен')
while True:
    try:  # добавляем try для бесперебойной работы
        current_time = time.strftime('%H:%M:%S', time.localtime())
        remind_times = ['11:00:00', '15:00:00', '19:00:00']
        if current_time in remind_times:
            print('remind_congratulate() - Start')
            remind_congratulate()
    except:
        print('time.sleep(1) - Done')

        time.sleep(10)  # в случае падения
