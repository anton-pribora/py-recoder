import fnmatch
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
import os

"""
Вкладка "перекодировать файлы" 
"""


def init_frame(self, frame: tk.Frame):
    """
    Инициализация вкладки "Перекодировать файлы"

    :param tk_recoder.gui.Gui self: Основное окно программы
    :param frame: Контейнер вкладки
    :return: None
    """

    config = self.config['files_converter']

    # Основной контейнер для формы поиска
    # ------------------------
    search_form = tk.Frame(frame)
    search_form.pack(fill='x', padx=10, pady=(10, 0))

    tk.Label(search_form, text='Путь поиска').grid(column=0, row=0, sticky='e')
    tk.Label(search_form, text='Маска').grid(column=0, row=1, sticky='e')

    # Каталог поиска файлов
    # ------------------------
    def update_path(*args):
        config['path'] = fc_path_var.get()

    fc_path_var = tk.StringVar(value=str(config['path']))
    fc_path_var.trace('w', update_path)

    self.fc_path = tk.Entry(search_form, textvariable=fc_path_var)
    self.fc_path.grid(column=1, row=0, padx=5, sticky='ew')
    self.fc_path.bind('<Return>', lambda *args: find_files())
    self.fc_path.bind('<KP_Enter>', lambda *args: find_files())

    # Маска для поиска файлов
    # ------------------------
    def update_mask(*args):
        config['mask'] = fc_mask_var.get()

    fc_mask_var = tk.StringVar(value=str(config['mask']))
    fc_mask_var.trace('w', update_mask)

    self.fc_mask = tk.Entry(search_form, textvariable=fc_mask_var)
    self.fc_mask.grid(column=1, row=1, padx=5, sticky='ew')
    self.fc_mask.bind('<Return>', lambda *args: find_files())
    self.fc_mask.bind('<KP_Enter>', lambda *args: find_files())

    self.fc_working = False

    def disable_controls(disabled: bool):
        """Отключение кнопок в зависимости от текущего состояния"""
        self.fc_mask.configure(state=('normal', 'disabled')[disabled])
        self.fc_path.configure(state=('normal', 'disabled')[disabled])
        self.fc_button_opendir.configure(state=('normal', 'disabled')[disabled])
        self.fc_button_search.configure(state=('normal', 'disabled')[disabled])
        self.fc_button_stop.configure(state=('normal', 'disabled')[not disabled])
        self.fc_enc_from.configure(state=('normal', 'disabled')[disabled])
        self.fc_enc_to.configure(state=('normal', 'disabled')[disabled])
        self.fc_button_recode.configure(state=('normal', 'disabled')[disabled])
        self.fc_save_origin.configure(state=('normal', 'disabled')[disabled])
        self.fc_origin_ext.configure(state=('normal', 'disabled')[disabled])
        self.fc_button_clear.configure(state=('normal', 'disabled')[disabled])
        self.fc_working = disabled

    def select_path():
        """Выбор каталога для поиска файлов"""
        result = filedialog.askdirectory(initialdir=self.fc_path.get(), mustexist=True)
        if result:
            self.fc_path.delete(0, tk.END)
            self.fc_path.insert(tk.END, result)

    def find_files(folder=None):
        """Поиск файлов в каталоге и его подкаталогах по маске"""
        found = 0
        current_list = list(self.fc_files.get(0, tk.END))
        disable_controls(True)
        mask = self.fc_mask.get()

        for root, dirs, files in os.walk(folder or self.fc_path.get(), topdown=False):
            self.update_status('Поиск в {folder}'.format(folder=root))

            for name in files:
                if mask == '' or fnmatch.fnmatch(name, mask):
                    path = os.path.join(root, name)
                    if path not in current_list:
                        found += 1
                        self.fc_files.insert(tk.END, path)
                        self.update_status('Добавлен файл: {path}'.format(path=path))
                    else:
                        self.update_status('Пропущен файл: {path}'.format(path=path))

            if not self.fc_working:
                break

        disable_controls(False)
        self.update_status('Добавлено файлов: {found}'.format(found=found))

    # Выбор исходной папки
    # ------------------------
    self.fc_button_opendir = tk.Button(search_form, text='Обзор', command=select_path)
    self.fc_button_opendir.grid(column=2, row=0, sticky=tk.EW, padx=5, pady=(0, 5))

    # Кнопка "найти файлы"
    # ------------------------
    self.fc_button_search = tk.Button(search_form, text='Найти', command=find_files)
    self.fc_button_search.grid(column=2, row=1, sticky=tk.EW, padx=5, pady=(0, 5))

    # Кнопка "остановить"
    # ------------------------
    def stop_working():
        self.fc_working = False

    self.fc_button_stop = tk.Button(search_form, text='Остановить', command=stop_working, state='disabled')
    self.fc_button_stop.grid(column=3, row=1, padx=5)

    search_form.columnconfigure(1, weight=1)

    # Фрейм "обработка файлов"
    # ------------------------
    handle_files = ttk.LabelFrame(frame, text='Обработка файлов', padding=(10, 5, 10, 10))
    handle_files.pack(fill='both', expand=1, pady=(5, 10), padx=10)

    buttons_bar1 = tk.Frame(handle_files)
    buttons_bar1.pack(fill='x')

    # Выбор исходной кодировки
    # ------------------------
    def update_enc_from(*args):
        config['enc_from'] = enc_from.get()

    tk.Label(buttons_bar1, text='Исходная кодировка').pack(side='left')
    enc_from = tk.StringVar(self)
    enc_from.set(str(config['enc_from']))
    enc_from.trace('w', update_enc_from)
    self.fc_enc_from = ttk.OptionMenu(buttons_bar1, enc_from, enc_from.get(), *self.recoder.text_encodings)
    self.fc_enc_from.pack(side='left', padx=(5, 10))

    # Выбор конечной кодировки
    # ------------------------
    def update_enc_to(*args):
        config['enc_to'] = enc_to.get()

    tk.Label(buttons_bar1, text='Конечная').pack(side='left')
    enc_to = tk.StringVar(self)
    enc_to.set(str(config['enc_to']))
    enc_to.trace('w', update_enc_to)
    self.fc_enc_to = ttk.OptionMenu(buttons_bar1, enc_to, enc_to.get(), *self.recoder.file_encodings)
    self.fc_enc_to.pack(side='left', padx=(5, 10))

    # Кнопка "перекодировать"
    # ------------------------
    def on_progress(text):
        self.update_status(text)
        return True if self.fc_working else False

    def convert_files(*args):
        position = 0
        errors = 0

        disable_controls(True)

        while position < self.fc_files.size():
            if not self.fc_working:
                break

            file = self.fc_files.get(position)
            self.update_status('Обработка файла: {file}'.format(file=file))

            success, error = self.recoder.convert_file(
                enc_from=enc_from.get(),
                enc_to=enc_to.get(),
                file_path=file,
                save_origin=save_origin.get(),
                origin_ext=origin_ext.get(),
                progress_callback=on_progress
            )

            if success:
                self.fc_files.delete(position)
            else:
                position += 1
                errors += 1

        disable_controls(False)

        if errors > 0:
            self.update_status('При обработке файлов возникли ошибки, обратитесь к логу для подробностей')
        else:
            self.update_status('Обработка завершена')

    self.fc_button_recode = tk.Button(buttons_bar1, text='Перекодировать', command=convert_files)
    self.fc_button_recode.pack(side='left')

    buttons_bar2 = tk.Frame(handle_files)
    buttons_bar2.pack(fill='x', pady=5)

    # Кнопка "очистить список"
    # ------------------------
    def clear_files():
        self.fc_files.delete(0, tk.END)
        self.update_status('Список очищен')

    self.fc_button_clear = tk.Button(buttons_bar2, text='Очистить список', command=clear_files)
    self.fc_button_clear.pack(side='left')

    # Галочка "сохранить оригинал"
    # ------------------------
    def update_save_origin(*args):
        config['save_origin'] = str(save_origin.get())

    save_origin = tk.BooleanVar(value=config['save_origin'].lower() in ['true', '1'])
    self.fc_save_origin = tk.Checkbutton(buttons_bar2, variable=save_origin, text='Сохранять оригинал с расширением')
    self.fc_save_origin.pack(side='left', padx=(10, 5))
    save_origin.trace('w', update_save_origin)

    # Выбор расширения для оригинального файла
    # ------------------------
    def update_origin_ext(*args):
        config['origin_ext'] = origin_ext.get()

    origin_ext = tk.StringVar(value=str(config['origin_ext']))
    origin_ext_values = ('~', '.bak', '.tmp', '.orig')
    self.fc_origin_ext = ttk.Combobox(buttons_bar2, textvariable=origin_ext, values=origin_ext_values)
    self.fc_origin_ext.pack(side='left')
    origin_ext.trace('w', update_origin_ext)

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

    self.fc_files = tk.Listbox(list_frame, selectmode='extended',
                               yscrollcommand=list_scroll_v.set,
                               xscrollcommand=list_scroll_h.set)
    self.fc_files.grid(column=0, row=0, sticky=tk.NSEW)

    list_scroll_v.configure(command=self.fc_files.yview)
    list_scroll_h.configure(command=self.fc_files.xview)

    def open_file(*args, **kwargs):
        for i in self.fc_files.curselection():
            path = self.fc_files.get(i)
            try:
                with open(path, 'r', encoding=enc_from.get(), newline='') as file:
                    text = file.read(1024 * 1024)
                    self.tc_text_from.delete('1.0', tk.END)
                    self.tc_text_from.insert(tk.INSERT, text)
                    self.tabs.select(0)
                    self.update_status('Открыт файл {path} в кодировке {enc}'.format(path=path, enc=enc_from.get()))
            except Exception as e:
                self.update_status('Ошибка: {error}'.format(error=str(e)))

    def delete_selected(*args, **kwargs):
        selected = self.fc_files.curselection()
        for i in selected[::-1]:
            self.fc_files.delete(i)
        self.update_status('Удалено файлов из списка: {number}'.format(number=len(selected)))

    def select_all(*args, **kwargs):
        self.fc_files.selection_set(0, tk.END)

    def drop_files(event):
        current_list = list(self.fc_files.get(0, tk.END))

        for path in self.fc_files.tk.splitlist(event.data):
            if os.path.isdir(path):
                find_files(path)
            elif os.path.isfile(path):
                if path not in current_list:
                    self.fc_files.insert(tk.END, path)
                    self.update_status('Добавлен файл: {file}'.format(file=path))

    self.fc_files.drop_target_register(DND_FILES)
    self.fc_files.dnd_bind('<<Drop>>', drop_files)

    self.fc_files.bind('<Double-1>', open_file)
    self.fc_files.bind('<Delete>', delete_selected)
    self.fc_files.bind('<Control-a>', select_all)
