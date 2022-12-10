# import required modules as numpy,
# matplotlib and radiobutton widget
import math
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Button

Q = 0.00001  # Ковариацию шума также можно понимать как отклонение шума между двумя моментами
R = 0.1  # Ковариацию состояния можно понимать как отклонение состояния между двумя моментами
P_k_k1 = 1  # Ковариация состояния в предыдущий момент
Kg = 0  # Калман Усиление
P_k1_k1 = 1
x_k_k1 = 0  # Значение состояния в предыдущий момент
ADC_OLD_Value = 0  # Последнее значение АЦП
kalman_adc_old = 0  # Наилучшая оценка последнего фильтра Калмана
matrix = []

def kalman(ADC_Value):
    global kalman_adc_old  # Определите две глобальные переменные, которые можно напрямую изменить в программе
    global P_k1_k1
    Z_k = ADC_Value  # Измерения

    if (
            abs(kalman_adc_old - ADC_Value) >= 80):  # Разница между последним значением состояния и измеренным значением в данный момент слишком велика, выполните простую фильтрацию первого порядка, золотое сечение 0618 может быть установлено по желанию
        x_k1_k1 = ADC_Value * 0.382 + kalman_adc_old * 0.618
    else:  # Разрыв не большой прямого использования
        x_k1_k1 = kalman_adc_old

    x_k_k1 = x_k1_k1  # Измерения
    P_k_k1 = P_k1_k1 + Q  # Формула два
    Kg = P_k_k1 / (P_k_k1 + R)  # Формула три

    kalman_adc = x_k_k1 + Kg * (Z_k - kalman_adc_old)  # Рассчитать наилучшую оценку
    P_k1_k1 = (1 - Kg) * P_k_k1  # Формула пятая
    P_k_k1 = P_k1_k1  # Обновление ковариации статуса

    ADC_OLD_Value = ADC_Value
    kalman_adc_old = kalman_adc
    return kalman_adc
def Reader():
	filetypes = (
        ('text files', '*.txt')
	)
	filename = filedialog.askopenfilename( title='Select file with your input data', filetypes=filetypes)
	global matrix
	file1 = open(filename, "r")
	
	lines = file1.readlines()
	matrix = []
	for line in lines:
		temp = line.replace(',', '').replace(';', '').replace('\n', '').split(' ')
		box = []
		for x in temp:
			if(x != ''):
				box.append(float(x))
		matrix.append(box)
	file1.close
Reader()

i = 0                                                     # изменяем этот параметр
arr = []
arr_x = []
for j in matrix:
    count = 0
    for k in j:
        if (count == i):
            arr_x.append(len(arr_x))
            arr.append(k)
        count = count + 1   
adc = []
for k in arr:
	adc.append(kalman(k))
fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(20)
l, = ax.plot(arr_x, arr, color='yellow')
kal, = ax.plot(arr_x, adc, color='red')
l.set_label('Noise')
kal.set_label('Kalman')
plt.subplots_adjust(left=0.4)
ax.set_title('Data',
			fontsize=18)

# sub-plot for radio button with
# left, bottom, width, height values
rax = plt.axes([0.01, 0.01, 0.3, 0.7])
radio_button = RadioButtons(rax, ('timesec',
								'SOG',
								'COG',
								'roll',
        						'pitch',
              					'yaw',
								'MC',
								'ax',
								'ay',
        						'RPM',
              					'rudder',
								'RPM_2',
								'rudder_2',
								'ROT',
        						'lat',
              					'lon',
								'magX',
								'magY',
								'next_wp',
        						'crs_err',
              					'app_xte',
								'rudder_value_2-55',
								'rudder_value_1-55'))

# function performed on switching the
# radiobuttons
map = {
		'timesec' : 0,
		'SOG':1,
		'COG':2,
		'roll':3,
        'pitch':4,
        'yaw':5,
		'MC':6,
		'ax':7,
		'ay':8,
        'RPM':9,
        'rudder':10,
		'RPM_2':11,
		'rudder_2':12,
		'ROT':13,
    	'lat':14,
        'lon':15,
		'magX':16,
		'magY':17,
		'next_wp':18,
        'crs_err':19,
        'app_xte':20,
		'rudder_value_2-55':21,
		'rudder_value_1-55':22
}
def colorfunc(label):
	Q = 0.00001  # Ковариацию шума также можно понимать как отклонение шума между двумя моментами
	R = 0.1  # Ковариацию состояния можно понимать как отклонение состояния между двумя моментами
	P_k_k1 = 1  # Ковариация состояния в предыдущий момент
	Kg = 0  # Калман Усиление
	P_k1_k1 = 1
	x_k_k1 = 0  # Значение состояния в предыдущий момент
	ADC_OLD_Value = 0  # Последнее значение АЦП
	kalman_adc_old = 0
	arr2 = []
	for j in matrix:
		count = 0
		for k in j:
			if (count == map[label]):
				arr2.append(k)
			count = count + 1  
	#l.set_color('red')
	l.set_data(arr_x, arr2)
	ax.set_ylim(min(arr2) - 10, max(arr2) + 10)
	adc2 = []
	for k in arr2:
		adc2.append(kalman(k))
	kal.set_ydata(adc2)
	plt.draw()

radio_button.on_clicked(colorfunc)
ax.legend()
plt.show()