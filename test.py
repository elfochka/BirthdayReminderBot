import time

now_date = time.localtime()
now_date = time.strftime('%d.%m', time.localtime())

print(now_date)