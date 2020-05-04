"""

    DeepGender - простая нейронная сеть, которую можно использовать
    для обучения на простых и крупных данных.

    Output - заточен под исключительно под пол, но при желании можно переписать
    и под работу с данными mnist.

    Разработчик Aveocr
    https://github.com/DenisCompany/

"""
import sys
import numpy as np
np.random.seed(1)

# линейные функции
def sigmoid(x):
    return 1 / np.exp(-x)
def sigmoid2derive(output):
    return output * (1-output)

# Набор для обучение нейронной сети

# Данные, которые пойдут на обучения
test_input = np.array([
         [16, 65, 169], # man
         [17, 49, 163], # woman
         [17, 72, 175], # man
         [20, 58, 171], # woman
         [20, 80, 181], # man
         [21, 69, 175], # man
         [22, 49, 164], # woman
         [22, 79, 185], # man
         [22, 72, 275], # man
         [20, 53, 165], # woman
         [21, 36, 163], # woman
         [24, 46, 169], # woman
         [24, 70, 180], # man
         [27, 74, 176], # man
         [29, 75, 179], # man
         [30, 57, 172], # woman
         [34, 63, 175], # woman
         [33, 73, 181], # man
         [30, 73, 173], # man
         [35, 62, 172], # woman
         [29, 70, 180], # woman
         [34, 65, 182], # woman
         [44, 72, 177], # man
         [42, 74, 181], # man
         [39, 62, 171], # woman
         [42, 64, 170], # woman
         [46, 55, 170], # woman
         [51, 73, 175], # man
         [54, 69, 178], # man
         [52, 59, 170], # woman
         [60, 64, 169], # woman
         [52, 72, 178]  # man
        ])
# Резльтутат который должен получиться
test_output = np.array([1,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,1]).T

# Обучение нейронной сети
def study(input, output, epoch, study=0):
    """
        * - обязательный параметр

        *input - входные данный нейронной сети.
        Данная нейронная сеть не предназначена
        Для обучения на крупных данных, тк она
        довольно медленная и не оптимизированная.


        *output - то, что нейронная сеть должна получить
        На выходе.

        *epoch - сколько раз будет обучаться сеть.
        Указанное число будет умножено на 10, то есть
        Если надо указать число 8, то надо написать 0.8

        study - режим отображение процесса обучения.
        По умолчанию он всегда равен 0

        На данный момент обучение происходит с помощью
        Линейной функцией sigmoid, соответсвенно выходные
        Данные будут нецелые числа от 0 до 1. Для корректной
        Работы рекомендуется использовать типы данных double

    """
    hidden_size = input.shape[0]
    row = input.shape[1]
    alpha = 0.01
    weights_0_1 = alpha * np.random.random((3, hidden_size)) - alpha
    weights_1_2 = 0.1 * np.random.random((hidden_size, 1)) - 0.1

    epoch *= 10
    # обучение нейронной сети
    for j in range(int(epoch)):
        for i in range(len(input)):
            # предсказание
            layer_0 = input[i:i+1]
            layer_1 = sigmoid(np.dot(layer_0, weights_0_1))
            layer_2 = np.dot(layer_1, weights_1_2)

            # Вычисление ошибки
            layer_2_error = np.sum((layer_2 - output[i:i+1])) ** 2

            layer_2_delta = layer_2 - output[i:i+1]
            layer_1_delta = layer_2_delta.dot(weights_1_2.T) \
                                      * sigmoid2derive(layer_1)

            # Корректировка веса для повышения точности результата
            weights_1_2 -= alpha * layer_1.T.dot((layer_2_delta))
            weights_0_1 -= alpha * layer_2.T.dot((layer_1_delta))

        # если включен процесс обучения
        if study != 0 and (j % 10 == 0 or j == (epoch-1)):
            # Показываем точность прогноза и ошибку
            print("I:" + str(j) + "\tПредсказание : " + str(layer_2[0])\
                  + "\tОшибка: " + str(layer_2_error), end="\n")
    return weights_0_1, weights_1_2

# Выводит какому полу принадлежит
def output(age, weight, height):

    weights_0_1, weights_1_2 = study(test_input, test_output, 10)
    # Предсказание нейронной сети насчет данных
    input = np.array([age, weight, height])
    layer_1 = sigmoid(np.dot(input, weights_0_1))
    layer_2 = np.dot(layer_1, weights_1_2)

    if (round(layer_2[0]) == 1):
        gender = 'Мужчина'
    else :
        gender = 'Женщина'
    return gender
