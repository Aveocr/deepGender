from random import randint
import datetime
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode

import neural_network as nn
from neural_network import *

datetime = datetime.datetime.now()

# Токен авторизации в группе
token = ""
# авторизация в группе
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# процесс начала
# 0 - диалог еще не начат
# 1 - диалог начат
# 2 - запущен процесс обрабоки сообщения
start = 0

# отправка собщения
# id - id пользователя вконтакте event.user_id (str)
# message - сообщение, которое я хочу отправить (str)
def message(id, message):
    vk.messages.send(
        random_id = randint(0, 2**32),
        user_id = event.user_id,
        message = message
    )

def check_error(age=None, weight=None, height=None):
    # Если пользователь не ввел одно меню
    try:
        if age == None or weight == None or height == None:
            return ("Прости, но ты забыл что-то ввести! \n " +
                    "Советую перепроверить, что ты ввел!" +
                    "Ты должен ввести свой возраст, вес в килограммах и рост в сантиметрах" +
                    "в том порядке, что я написал и через запитую\n\n" +
                    "Вот пример: 21, 71, 175")

        # обработка возраста
        elif int(age) < 14 or int(weight) < 40 or int(height) < 150:
            return "Прости, но ты слишком маленький\n\nПовтори попытку"
        elif int(age) > 70 or int(weight) > 140 or int(height) > 235:
            return "Прости, но ты слишком взрослый/крупный/высокий.\n\nПовтори попытку"
        else :
            return 1
    except ValueError:
        return ("Походу ты ввел не цифры! " +
                "\nСоветую повторить попытку, иначе будет плохо!")

if __name__ == '__main__':
    for event in longpoll.listen():
        #Слушаем longpoll, если пришло сообщение то:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Если есть сообщение
            if event.text:
                # Если написали в ЛС
                if event.from_user:
                    # Имя человека
                    first_name = vk.users.get(
                          user_ids=event.user_id,
                          fields='first_name',
                          name_case='nom') # 'nom' - иминительный падеж
                    for i in first_name: first_name = i["first_name"]

                    # Сохранение в лог
                    with open("log.txt", 'a') as file:
                        file.write("Date: " + str(datetime.day) + "." + str(datetime.month) + "." + str(datetime.year)
                        + " time:" + str(datetime.hour) + ":" + str(datetime.minute)
                        + ' id: ' + str(event.user_id) + " first_name: " + str(first_name) + "\n")

                    # Отправка сообщения
                    start = 1
                    message(event.user_id,
                    "Привет, " + first_name + "!.\n Ты хочешь протестировать нейронную " +
                    "сеть и узнать, какой был бы у тебя пол в Нарнии? Напиши да или нет")

                # Если пользователь согласен, кто он
                elif (event.text.lower() == "да" and start == 1):
                    # Отправка сообщения
                    start = 2
                    message(event.user_id,
                    "Отлично, тогда пришли мне свой возраст, вес в килограммах и рост в сантиметрах" +
                    "в том порядке, что я написал и через запитую\n\n" +
                    "Вот пример: 21, 71, 175\n\nЧтобы выйти напиши \"выход\"" )
                # Когда пользователь введ данные
                elif ( (event.text.lower() == 'выход'  \
                      or event.text.lower() == 'хватит' \
                      or event.text.lower() == 'стоп' \
                      or event.text.lower() == 'прекратить' ) \
                      and start == 2):
                      message(event.user_id, "Окей, не хочешь, как хочешь. Пока")
                      start = 0
                # Начинаем процесс обработки массива
                elif (event.text and start == 2):
                    # Переводим введенную информацию в массив
                    date = event.text.replace(" ", "").split(",")
                    try:
                        check = check_error(int(date[0]), int(date[1]), int(date[2]))
                    except IndexError:
                        check = 0
                    except ValueError:
                        check = 2
                    # если все норм, то
                    if check == 0:
                        message(event.user_id,
                        "Прости, но ты забыл что-то ввести! \n " +
                        "Советую перепроверить, что ты ввел!" +
                        "Ты должен ввести свой возраст, вес в килограммах и рост в сантиметрах" +
                        "в том порядке, что я написал и через запитую\n\n" +
                        "Вот пример: 21, 71, 175")
                    elif check == 1:
                        result = nn.output(int(date[0]), int(date[1]), int(date[2]))
                        message(event.user_id, "Поздравляем! \nВаш пол в нарнии: "
                                    + result + "\n\nХочешь попробывать еще раз? Напиши да или нет")
                        start = 1
                    elif check == 2:
                        message(event.user_id,
                            "Походу ты ввел не цифры! " +
                            "\nСоветую повторить попытку, иначе будет плохо!")
                    else :
                        message(event.user_id, check)

                # событие выхода
                elif (event.text.lower() == "нет" and start == 1):
                    start = 0
                    vk.messages.send(
                        random_id = randint(0, 2**32),
                        user_id = event.user_id,
                        message = "Ну ладно((((\n Я напишу тебе, когда что-нибудь " \
                        "новое появится")

            else :
                vk.messages.send( #Отправляем сообщение
                    random_id = randint(0, 2**64),
                    user_id=event.user_id,
                    message='Прости, но я тебя не понимаю'
                )
