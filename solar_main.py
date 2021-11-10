# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import solar_vis as vis
import solar_model as model
import solar_input as in_put


class GlobalVariablesMain:
    """класс глобальных переменных этого файла"""

    perform_execution = False
    """Флаг цикличности выполнения расчёта"""

    physical_time = 0
    """Физическое время от начала расчёта.
    Тип: float"""

    displayed_time = None
    """Отображаемое на экране время.
    Тип: переменная tkinter"""

    time_step = None
    """Шаг по времени при моделировании.
    Тип: float"""

    time_speed = None
    """Ползунок скорости промотки времени на экране"""

    space = None
    """Полотно для прорисовки"""

    start_button = None
    """Кнопка старт/пауза"""

    space_objects = []
    """Список космических объектов."""


glob = GlobalVariablesMain


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной glob.perform_execution.
    При glob.perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    model.recalculate_space_objects_positions(glob.space_objects, glob.time_step.get())
    for body in glob.space_objects:
        vis.update_object_position(glob.space, body)
    glob.physical_time += glob.time_step.get()
    glob.displayed_time.set("%.1f" % glob.physical_time + " seconds gone")

    if glob.perform_execution:
        glob.space.after(101 - int(glob.time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    glob.perform_execution = True
    glob.start_button['text'] = "Pause"
    glob.start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    glob.perform_execution = False
    glob.start_button['text'] = "Start"
    glob.start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список glob.space_objects
    """
    glob.perform_execution = False
    for obj in glob.space_objects:
        glob.space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    glob.space_objects = in_put.read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in glob.space_objects])
    vis.calculate_scale_factor(max_distance)

    for obj in glob.space_objects:
        if obj.type == 'star':
            vis.create_star_image(glob.space, obj)
        elif obj.type == 'planet':
            vis.create_planet_image(glob.space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию записи параметров системы небесных тел в данный файл.
    Считанные объекты сохраняются из списка glob.space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    in_put.write_space_objects_data_to_file(out_filename, glob.space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    print('Modelling started!')
    glob.physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    glob.space = tkinter.Canvas(root, width=vis.WINDOW_WIDTH, height=vis.WINDOW_HEIGHT, bg="white")
    glob.space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    glob.start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    glob.start_button.pack(side=tkinter.LEFT)

    # вводим временной шаг для рассчетов
    glob.time_step = tkinter.DoubleVar()
    glob.time_step.set(1)
    glob.time_step_entry = tkinter.Entry(frame, textvariable=glob.time_step)
    glob.time_step_entry.pack(side=tkinter.LEFT)

    # ползунок скорости перемотки времени
    glob.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=glob.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    # кнопки открытия файла и записывания в файл
    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    # вывод прошедшего времени
    glob.displayed_time = tkinter.StringVar()
    glob.displayed_time.set(str(glob.physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=glob.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()
