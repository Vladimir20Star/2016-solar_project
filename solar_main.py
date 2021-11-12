# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import solar_vis as vis
import solar_model as model
import solar_input as in_put


class SolarProject:
    def __init__(self):
        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""

        self.physical_time = 0
        """Физическое время от начала расчёта.
        Тип: float"""

        self.displayed_time = None
        """Отображаемое на экране время.
        Тип: переменная tkinter"""

        self.time_step = None
        """Шаг времени при моделировании.
        Тип: float"""

        self.time_step_entry = None
        """Переменная для поля ввода шага времени"""

        self.time_speed = None
        """Ползунок скорости промотки времени на экране"""

        self.max_distance = None

        self.space = None
        """Полотно для прорисовки"""

        self.start_button = None
        """Кнопка старт/пауза"""

        self.space_objects = []
        """Список космических объектов."""

    def execution(self):
        """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
        а также обновляя их положение на экране.
        Цикличность выполнения зависит от значения глобальной переменной self.perform_execution.
        При self.perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
        """
        model.recalculate_space_objects_positions(self.space_objects, self.time_step.get(), self.max_distance)
        for body in self.space_objects:
            vis.update_object_position(self.space, body)
        self.physical_time += self.time_step.get()
        self.displayed_time.set("%.1f" % self.physical_time + " seconds gone")

        if self.perform_execution:
            self.space.after(101 - int(self.time_speed.get()), self.execution)

    def start_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution.
        """
        self.perform_execution = True
        self.start_button['text'] = "Pause"
        self.start_button['command'] = self.stop_execution

        self.execution()
        print('Started execution...')

    def stop_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Останавливает циклическое исполнение функции execution.
        """
        self.perform_execution = False
        self.start_button['text'] = "Start"
        self.start_button['command'] = self.start_execution
        print('Paused execution.')

    def open_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список self.space_objects
        """
        self.perform_execution = False
        for obj in self.space_objects:
            self.space.delete(obj.image)  # удаление старых изображений планет
        in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
        self.space_objects = in_put.read_space_objects_data_from_file(in_filename)
        self.max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in self.space_objects])
        vis.scale.calculate_scale_factor(self.max_distance)

        for obj in self.space_objects:
            if obj.type == 'star':
                vis.create_star_image(self.space, obj)
            elif obj.type == 'planet':
                vis.create_planet_image(self.space, obj)
            else:
                raise AssertionError()

    def save_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию записи параметров системы небесных тел в данный файл.
        Считанные объекты сохраняются из списка self.space_objects
        """
        out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
        in_put.write_space_objects_data_to_file(out_filename, self.space_objects)

    def main(self):
        """Главная функция главного модуля.
        Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
        """
        print('Modelling started!')
        self.physical_time = 0

        root = tkinter.Tk()
        # космическое пространство отображается на холсте типа Canvas
        self.space = tkinter.Canvas(root, width=vis.WINDOW_WIDTH, height=vis.WINDOW_HEIGHT, bg="white")
        self.space.pack(side=tkinter.TOP)
        # нижняя панель с кнопками
        frame = tkinter.Frame(root)
        frame.pack(side=tkinter.BOTTOM)

        self.start_button = tkinter.Button(frame, text="Start", command=self.start_execution, width=6)
        self.start_button.pack(side=tkinter.LEFT)

        # вводим временной шаг для рассчетов
        self.time_step = tkinter.DoubleVar()
        self.time_step.set(1)
        self.time_step_entry = tkinter.Entry(frame, textvariable=self.time_step)
        self.time_step_entry.pack(side=tkinter.LEFT)

        # ползунок скорости перемотки времени
        self.time_speed = tkinter.DoubleVar()
        scale = tkinter.Scale(frame, variable=self.time_speed, orient=tkinter.HORIZONTAL)
        scale.pack(side=tkinter.LEFT)

        # кнопки открытия файла и записывания в файл
        load_file_button = tkinter.Button(frame, text="Open file...", command=self.open_file_dialog)
        load_file_button.pack(side=tkinter.LEFT)
        save_file_button = tkinter.Button(frame, text="Save to file...", command=self.save_file_dialog)
        save_file_button.pack(side=tkinter.LEFT)

        # вывод прошедшего времени
        self.displayed_time = tkinter.StringVar()
        self.displayed_time.set(str(self.physical_time) + " seconds gone")
        time_label = tkinter.Label(frame, textvariable=self.displayed_time, width=30)
        time_label.pack(side=tkinter.RIGHT)

        root.mainloop()
        print('Modelling finished!')


if __name__ == "__main__":
    project = SolarProject()
    project.main()
