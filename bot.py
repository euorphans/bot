import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def send_message(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

token = "9c21fca28aeb51965f4eed762926d4c2cdd99748db9061804d979989438621964d100b85aeb877f183402"
vk = vk_api.VkApi(token=token)

data = VkLongPoll(vk)

for event in data.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            text = event.text
            text = text.split()

            if text[0] == "/help":
                send_message(event.user_id, "/ст + ник - статистика игроков")
            elif text[0] == "/ст":
                response = requests.get(f'https://api.vimeworld.ru/user/name/{text[1]}').json()[0]

                if response['guild']:
                    guild = response['guild']['name']
                else:
                    guild = "Отсутствует"

                days = str(response['playedSeconds']/60/60/24).split(".")[0]
                hour = str(response['playedSeconds']/60/60%24).split(".")[0]
                min = str(response['playedSeconds']/60%60).split(".")[0]
                sec = str(response['playedSeconds']%60).split(".")[0]


                if response['id']:
                    player = f" {response['username']}" \
                             f"\n {response['rank']}" \
                             f"\n {guild}" \
                             f"\n {days} дн. {hour} ч. {min} мин. {sec} сек."
                else:
                    player = f"Такого игрока не существует!"
                send_message(event.user_id, player)
            elif text[0] == "/streams" or text[0] == "/стримы":
                response = requests.get(f'https://api.vimeworld.ru/online/streams').json()