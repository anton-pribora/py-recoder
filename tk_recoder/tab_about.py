import tkinter as tk
import webbrowser
from functools import partial

"""
Вкладка "перекодировать текст" 
"""


def init_frame(self, frame: tk.Frame):
    """
    Инициализация вкладки "О программе"

    :param tk_recoder.gui.Gui self: Основное окно программы
    :param frame: Контейнер вкладки
    :return: None
    """

    labels = tk.Frame(frame)
    labels.pack(expand=1, fill='both', pady=10, padx=10)

    urls = {
        'Сайт': 'https://anton-pribora.ru/recoder/',
        'Github': 'https://github.com/anton-pribora/py-recoder',
        'Оставить отзыв': 'https://anton-pribora.ru/feedback/?subject=' + self.recoder.get_version()
    }

    row = 0

    def open_url(location, *args):
        webbrowser.open(location)

    for text, url in urls.items():
        label = tk.Label(labels, text=text)
        label.grid(column=0, row=row, padx=5, pady=3, sticky=tk.E)

        link = tk.Label(labels, text=url, fg='blue', cursor='hand2')
        link.grid(column=1, row=row, sticky=tk.W)
        link.bind("<Button-1>", partial(open_url, url))

        row += 1
