# from telethon import TelegramClient, sync
#
# # Вставляем api_id и api_hash
# api_id = 22833500
# api_hash = 'be9afc12bd3f71b4a07bb9e59056168c'
# print(1)
# client = TelegramClient('name', api_id, api_hash)
# print(1.2)
#
# client.start()
# print(2)
#
# for dialog in client.iter_dialogs():
#     print(dialog.title)
# print('')
# participants = client.get_participants('УПППП SberDevices')
# print(3)
#
# # print(participants)
# for user in participants:
#     print(user.id, end='/')
#     print(user.username, end='/')
#     print(user.first_name, end='/')
#     print(user.last_name)
# print(4)

from telethon import TelegramClient, sync

# Вставляем api_id и api_hash
api_id = 22242736
api_hash = 'a1ec460d6007cc469879aad3cdbb4b3e'
print(1)
client = TelegramClient('nameE', api_id, api_hash)
print(1.2)

client.start()
print(2)

for dialog in client.iter_dialogs():
    print(dialog.title)
print('')
participants = client.get_participants('УПППП SberDevices')
print(3)

# print(participants)
for user in participants:
    print(user.id, end='/')
    print(user.username, end='/')
    print(user.first_name, end='/')
    print(user.last_name)
print(4)

