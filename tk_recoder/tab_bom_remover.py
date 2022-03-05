import fnmatch
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
import os

"""
Вкладка "Убрать BOM" 
"""


def init_frame(self, frame: tk.Frame):
    """
    Инициализация вкладки "Убрать BOM"

    :param tk_recoder.gui.Gui self: Основное окно программы
    :param frame: Контейнер вкладки
    :return: None
    """

    config = self.config['bom_remover']

    # Основной контейнер для формы поиска
    # ------------------------
    search_form = tk.Frame(frame)
    search_form.pack(fill='x')

    tk.Label(search_form, text='Путь поиска').grid(column=0, row=0, sticky='e')
    tk.Label(search_form, text='Маска').grid(column=0, row=1, sticky='e')

    # Каталог поиска файлов
    # ------------------------
    def update_path(*args):
        config['path'] = br_path_var.get()

    br_path_var = tk.StringVar(value=str(config['path']))
    br_path_var.trace('w', update_path)

    self.br_path = tk.Entry(search_form, textvariable=br_path_var)
    self.br_path.grid(column=1, row=0, padx=5, sticky='ew')
    self.br_path.bind('<Return>', lambda *args: find_files())
    self.br_path.bind('<KP_Enter>', lambda *args: find_files())

    # Маска для поиска файлов
    # ------------------------
    def update_mask(*args):
        config['mask'] = br_mask_var.get()

    br_mask_var = tk.StringVar(value=str(config['mask']))
    br_mask_var.trace('w', update_mask)

    self.br_mask = tk.Entry(search_form, textvariable=br_mask_var)
    self.br_mask.grid(column=1, row=1, padx=5, sticky='ew')
    self.br_mask.bind('<Return>', lambda *args: find_files())
    self.br_mask.bind('<KP_Enter>', lambda *args: find_files())

    self.br_working = False

    def disable_controls(disabled: bool):
        """Отключение кнопок в зависимости от текущего состояния"""
        self.br_mask.configure(state=('normal', 'disabled')[disabled])
        self.br_path.configure(state=('normal', 'disabled')[disabled])
        self.br_button_opendir.configure(state=('normal', 'disabled')[disabled])
        self.br_button_search.configure(state=('normal', 'disabled')[disabled])
        self.br_button_stop.configure(state=('normal', 'disabled')[not disabled])
        self.br_button_recode.configure(state=('normal', 'disabled')[disabled])
        self.br_button_clear.configure(state=('normal', 'disabled')[disabled])
        self.br_working = disabled

    def select_path():
        """Выбор каталога для поиска файлов"""
        result = filedialog.askdirectory(initialdir=self.br_path.get(), mustexist=True)
        if result:
            self.br_path.delete(0, tk.END)
            self.br_path.insert(tk.END, result)

    def find_files(folder=None):
        """Поиск файлов в каталоге и его подкаталогах по маске"""
        found = 0
        current_list = list(self.br_files.get(0, tk.END))
        disable_controls(True)
        mask = self.br_mask.get()

        for root, dirs, files in os.walk(folder or self.br_path.get(), topdown=False):
            self.update_status('Поиск в {folder}'.format(folder=root))

            for name in files:
                if mask == '' or fnmatch.fnmatch(name, mask):
                    path = os.path.join(root, name)
                    if path not in current_list and self.recoder.file_has_bom(path):
                        found += 1
                        self.br_files.insert(tk.END, path)
                        self.update_status('Добавлен файл: {path}'.format(path=path))
                    else:
                        self.update_status('Пропущен файл: {path}'.format(path=path))

            if not self.br_working:
                break

        disable_controls(False)
        self.update_status('Добавлено файлов: {found}'.format(found=found))

    # Выбор исходной папки
    # ------------------------
    self.br_button_opendir = tk.Button(search_form, text='Обзор', command=select_path)
    self.br_button_opendir.grid(column=2, row=0, sticky=tk.EW, padx=5, pady=(0, 5))

    # Кнопка "найти файлы"
    # ------------------------
    self.br_button_search = tk.Button(search_form, text='Найти', command=find_files)
    self.br_button_search.grid(column=2, row=1, sticky=tk.EW, padx=5, pady=(0, 5))

    # Кнопка "остановить"
    # ------------------------
    def stop_working():
        self.br_working = False

    self.br_button_stop = tk.Button(search_form, text='Остановить', command=stop_working, state='disabled')
    self.br_button_stop.grid(column=3, row=1, padx=5)

    search_form.columnconfigure(1, weight=1)

    # Фрейм "обработка файлов"
    # ------------------------
    handle_files = ttk.LabelFrame(frame, text='Обработка файлов', padding=(10, 5, 10, 10))
    handle_files.pack(fill='both', expand=1, pady=(5, 0))

    buttons_bar1 = tk.Frame(handle_files)
    buttons_bar1.pack(fill='x')

    # Кнопка "очистить список"
    # ------------------------
    def clear_files():
        self.br_files.delete(0, tk.END)
        self.update_status('Список очищен')

    self.br_button_clear = tk.Button(buttons_bar1, text='Очистить список', command=clear_files)
    self.br_button_clear.pack(side='left')

    # Кнопка "Убрать BOM"
    # ------------------------
    def on_progress(text):
        self.update_status(text)
        return True if self.br_working else False

    def convert_files(*args):
        position = 0
        errors = 0

        disable_controls(True)

        while position < self.br_files.size():
            if not self.br_working:
                break

            file = self.br_files.get(position)
            self.update_status('Обработка файла: {file}'.format(file=file))

            success, error = self.recoder.remove_bom(
                file_path=file,
                progress_callback=on_progress
            )

            if success:
                self.br_files.delete(position)
            else:
                position += 1
                errors += 1

        disable_controls(False)

        if errors > 0:
            self.update_status('При обработке файлов возникли ошибки, обратитесь к логу для подробностей')
        else:
            self.update_status('Обработка завершена')

    self.br_button_recode = tk.Button(buttons_bar1, text='Убрать BOM', command=convert_files)
    self.br_button_recode.pack(side='left', padx=10)

    buttons_bar2 = tk.Frame(handle_files)
    buttons_bar2.pack(fill='x', pady=5)

    # Список файлов для перекодировки
    # ------------------------
    list_frame = tk.Frame(handle_files)
    list_frame.pack(fill='both', expand=1)
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    list_scroll_v = tk.Scrollbar(list_frame, orient='vertical')
    list_scroll_v.grid(column=1, row=0, sticky=tk.NS)

    list_scroll_h = tk.Scrollbar(list_frame, orient='horizontal')
    list_scroll_h.grid(column=0, row=1, sticky=tk.EW)

    self.br_files = tk.Listbox(list_frame, selectmode='extended',
                               yscrollcommand=list_scroll_v.set,
                               xscrollcommand=list_scroll_h.set)
    self.br_files.grid(column=0, row=0, sticky=tk.NSEW)

    list_scroll_v.configure(command=self.br_files.yview)
    list_scroll_h.configure(command=self.br_files.xview)

    def open_file(*args, **kwargs):
        for i in self.br_files.curselection():
            path = self.br_files.get(i)
            try:
                with open(path, 'r', encoding='utf-8-sig', newline='') as file:
                    text = file.read(1024 * 1024)
                    self.tc_text_from.delete('1.0', tk.END)
                    self.tc_text_from.insert(tk.INSERT, text)
                    self.tabs.select(0)
                    self.update_status('Открыт файл {path} в кодировке {enc}'
                                       .format(path=path, enc=self.recoder.utf8_bom_encoding))
            except Exception as e:
                self.update_status('Ошибка: {error}'.format(error=str(e)))

    def delete_selected(*args, **kwargs):
        selected = self.br_files.curselection()
        for i in selected[::-1]:
            self.br_files.delete(i)
        self.update_status('Удалено файлов из списка: {number}'.format(number=len(selected)))

    def select_all(*args, **kwargs):
        self.br_files.selection_set(0, tk.END)

    def drop_files(event):
        current_list = list(self.br_files.get(0, tk.END))

        for path in self.br_files.tk.splitlist(event.data):
            if os.path.isdir(path):
                find_files(path)
            elif os.path.isfile(path):
                if path not in current_list and self.recoder.file_has_bom(path):
                    self.br_files.insert(tk.END, path)
                    self.update_status('Добавлен файл: {file}'.format(file=path))

    self.br_files.drop_target_register(DND_FILES)
    self.br_files.dnd_bind('<<Drop>>', drop_files)

    self.br_files.bind('<Double-1>', open_file)
    self.br_files.bind('<Delete>', delete_selected)
    self.br_files.bind('<Control-a>', select_all)
