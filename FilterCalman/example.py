import numpy

import pylab

# Импортируем класс слайдера
from matplotlib.widgets import Slider, RadioButtons


def gauss(sigma, mu, x):
    '''Отображаемая фукнция'''
    return (1.0 / (sigma * numpy.sqrt(2.0 * numpy.pi)) *
            numpy.exp(-((x - mu) ** 2) / (2 * sigma * sigma)))


if __name__ == '__main__':
    def updateGraph():
        '''Функция для обновления графика'''
        # Будем использовать sigma и mu, установленные с помощью слайдеров
        global slider_sigma
        global slider_mu
        global graph_axes
        global radiobuttons_color

        colors = {'Красный': 'r', 'Синий': 'b', 'Зеленый': 'g'}

        # Используем атрибут val, чтобы получить значение слайдеров
        sigma = slider_sigma.val
        mu = slider_mu.val
        x = numpy.arange(-5.0, 5.0, 0.01)
        y = gauss(sigma, mu, x)

        style = colors[radiobuttons_color.value_selected]

        graph_axes.clear()
        graph_axes.plot(x, y, style)
        graph_axes.grid()
        pylab.draw()

    def onChangeGraph(value):
        '''Обработчик события изменения значений слайдеров'''
        updateGraph()

    def onRadioButtonsClicked(label):
        '''!!! Обработчик события при клике по RadioButtons'''
        updateGraph()

    # Создадим окно с графиком
    fig, graph_axes = pylab.subplots()
    graph_axes.grid()

    # Оставим снизу от графика место для виджетов
    fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.5)

    # Создание слайдера для задания sigma
    axes_slider_sigma = pylab.axes([0.05, 0.35, 0.85, 0.04])
    slider_sigma = Slider(axes_slider_sigma,
                          label='σ',
                          valmin=0.1,
                          valmax=1.0,
                          valinit=0.5,
                          valfmt='%1.2f')

    # Подпишемся на событие при изменении значения слайдера.
    slider_sigma.on_changed(onChangeGraph)

    # Создание слайдера для задания mu
    axes_slider_mu = pylab.axes([0.05, 0.27, 0.85, 0.04])
    slider_mu = Slider(axes_slider_mu,
                       label='μ',
                       valmin=-4.0,
                       valmax=4.0,
                       valinit=0.0,
                       valfmt='%1.2f')

    # Подпишемся на событие при изменении значения слайдера.
    slider_mu.on_changed(onChangeGraph)

    # !!! Создание осей для переключателей
    axes_radiobuttons = pylab.axes([0.05, 0.05, 0.2, 0.2])

    # !!! Создание переключателя
    radiobuttons_color = RadioButtons(axes_radiobuttons,
                                      ['Красный', 'Синий', 'Зеленый'])
    radiobuttons_color.on_clicked(onRadioButtonsClicked)

    updateGraph()
    pylab.show()