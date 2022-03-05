import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinter import filedialog
from functools import partial

"""
Вкладка "перекодировать текст" 
"""


def init_frame(self, frame: tk.Frame):
    """
    Инициализация вкладки "Перекодировать текст"

    :param tk_recoder.gui.Gui self: Основное окно программы
    :param frame: Контейнер вкладки
    :return: None
    """
    buttons = tk.Frame(frame)
    buttons.pack(fill='x', padx=10, pady=(10, 0))
    buttons.columnconfigure(5, weight=1)

    texts = tk.Frame(frame)
    texts.pack(fill='both', expand=1, pady=(10, 0), padx=10)

    self.tc_text_from = st.ScrolledText(texts, width=30, height=3)
    self.tc_text_from.pack(side='left', expand=1, fill='both', padx=(0, 2))
    self.tc_text_from.insert(tk.INSERT, "Привет мир!")

    self.tc_text_to = st.ScrolledText(texts, width=30, height=3)
    self.tc_text_to.pack(side='right', expand=1, fill='both', padx=(2, 0))

    ttk.Label(buttons, text='Исходная').grid(column=0, row=0)

    choices = self.recoder.text_encodings

    self.tc_enc_from = tk.StringVar(self)
    self.tc_enc_from.set(choices[0])
    ttk.OptionMenu(buttons, self.tc_enc_from, self.tc_enc_from.get(), *choices).grid(column=1, row=0, padx=(10, 20))

    ttk.Label(buttons, text='Конечная').grid(column=2, row=0)

    self.tc_enc_to = tk.StringVar(self)
    self.tc_enc_to.set(choices[0])
    ttk.OptionMenu(buttons, self.tc_enc_to, self.tc_enc_to.get(), *choices).grid(column=3, row=0, padx=(10, 20))

    def convert():
        self.tc_text_to.replace(1.0, tk.END, self.recoder.convert_text(self.tc_enc_from.get(),
                                                                       self.tc_enc_to.get(),
                                                                       self.tc_text_from.get(1.0, tk.END)))
        self.update_status(
            'Текст перекодирован из {enc_from} в {enc_to}'.format(enc_from=self.tc_enc_from.get(),
                                                                  enc_to=self.tc_enc_to.get()))

    enc_button = ttk.Button(buttons, text='Перекодировать', padding=(10, 3, 10, 3), command=convert)
    enc_button.grid(column=4, row=0)

    bt = tk.Menubutton(buttons, text='Сохранить как...', relief='raised', compound='right', padx=10)
    popup = tk.Menu(bt, tearoff=0)
    bt.configure(menu=popup)

    def save_as(encoding):
        try:
            file = filedialog.asksaveasfilename()
            if file:
                if encoding == self.recoder.utf8_bom_encoding:
                    file_encoding = 'utf-8-sig'
                else:
                    file_encoding = encoding

                with open(file, 'w', encoding=file_encoding, errors='replace') as fp:
                    fp.write(self.tc_text_to.get(1.0, tk.END))

                self.update_status('Данные в кодировке {enc} сохранены в файл {file}'.format(enc=encoding,
                                                                                             file=file))
        except Exception as err:
            self.update_status('Ошибка: {err}'.format(err=str(err)))

    for enc in self.recoder.file_encodings:
        popup.add_command(label=enc, command=partial(save_as, enc))

    frame.columnconfigure(5, weight=1)
    bt.grid(column=5, row=0, padx=10, sticky=tk.E)
