import numpy as np
import matplotlib.pyplot as plt

Q = 0.00001  # Ковариацию шума также можно понимать как отклонение шума между двумя моментами
R = 0.1  # Ковариацию состояния можно понимать как отклонение состояния между двумя моментами
P_k_k1 = 1  # Ковариация состояния в предыдущий момент
Kg = 0  # Калман Усиление
P_k1_k1 = 1
x_k_k1 = 0  # Значение состояния в предыдущий момент
ADC_OLD_Value = 0  # Последнее значение АЦП
kalman_adc_old = 0  # Наилучшая оценка последнего фильтра Калмана


def kalman(ADC_Value):
    global kalman_adc_old  # Определите две глобальные переменные, которые можно напрямую изменить в программе
    global P_k1_k1
    Z_k = ADC_Value  # Измерения

    if (
            abs(kalman_adc_old - ADC_Value) >= 80):  # Разница между последним значением состояния и измеренным значением в данный момент слишком велика, выполните простую фильтрацию первого порядка, золотое сечение 0618 может быть установлено по желанию
        x_k1_k1 = ADC_Value * 0.382 + kalman_adc_old * 0.618
    else:  # Разрыв не большой прямого использования
        x_k1_k1 = kalman_adc_old;

    x_k_k1 = x_k1_k1  # Измерения
    P_k_k1 = P_k1_k1 + Q  # Формула два
    Kg = P_k_k1 / (P_k_k1 + R)  # Формула три

    kalman_adc = x_k_k1 + Kg * (Z_k - kalman_adc_old)  # Рассчитать наилучшую оценку
    P_k1_k1 = (1 - Kg) * P_k_k1  # Формула пятая
    P_k_k1 = P_k1_k1  # Обновление ковариации статуса

    ADC_OLD_Value = ADC_Value
    kalman_adc_old = kalman_adc
    return kalman_adc


plt.figure(figsize=(20, 8))  # Создать размер холста (20,8)

file1 = open("/Users/iisuos/PyTest/input.txt", "r")
# считываем все строки
lines = file1.readlines()
matrix = []
# итерация по строкам
for line in lines:
    temp = line.replace(',', '').replace(';', '').replace('\n', '').split(' ')
    box = []
    for x in temp:
        if(x != ''):
            box.append(float(x))
    matrix.append(box)
    file1.close
# закрываем файл
i = 12                                                     # изменяем этот параметр
arr = []
for j in matrix:
    count = 0
    for k in j:
        if (count == i):
            arr.append(k)
        count = count + 1
        
plt.plot(arr, label='Noise')  # Рисуем помехи
adc = []
for k in arr:
    adc.append(kalman(k))

plt.plot(adc, label='Kalman')  # Kalman отфильтрованное изображение
plt.legend()  # Показать легенду
plt.show()
