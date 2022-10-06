import time
from BirthdayReminder import remind_congratulate


while True:
    try:  # добавляем try для бесперебойной работы
        current_time = time.strftime('%H:%M:%S', time.localtime())
        remind_times = ['11:00:00']
        # remind_times = ['11:00:00']
        if current_time in remind_times:
            remind_congratulate()
    except:
        time.sleep(10)  # в случае падения
