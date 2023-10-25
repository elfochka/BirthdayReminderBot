FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#COPY . .
COPY BirthdayReminder.py BirthdayReminderTimer.py /app/

# Запускаем
CMD ["/bin/bash", "-c", "python3 keys.py && sleep 1 && python3 BirthdayReminderTimer.py && python3 BirthdayReminder.py"]
#CMD ["/bin/bash", "-c", "python3 BirthdayReminderTimer.py && sleep 1 && python3 BirthdayReminder.py"]
#CMD [ "python3", "main.py" ]
