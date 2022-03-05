from recoder import Recoder
import tk_recoder.tab_text_converter
import tk_recoder.tab_files_converter
import tk_recoder.tab_about
import tk_recoder.tab_bom_remover
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD


class Gui(TkinterDnD.Tk):
    def __init__(self, recorder: Recoder, config):
        super().__init__()
        self.recoder = recorder
        self.config = config

        self.title(self.recoder.get_version())

        style = ttk.Style()
        current_theme = style.theme_use()
        style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [7, 4]}}})

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(padx=10, pady=(10, 3), fill='both', anchor='nw', expand=1)

        self.__init_tab1()
        self.__init_tab2()
        self.__init_tab3()
        self.__init_tab4()

        self.status_var = tk.StringVar()
        self.statusbar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        self.minsize(800, 500)
        self.geometry("800x500")

        self.tabs.select(1)

    def update_status(self, text):
        self.status_var.set(text)
        self.update()

    # Перекодировка текста
    def __init_tab1(self):
        tab = tk.Frame(self.tabs)
        tab.pack(fill='both', expand=1)
        self.tabs.add(tab, text="Перекодировать текст")
        tk_recoder.tab_text_converter.init_frame(self, tab)

    # Перекодировать файлы
    def __init_tab2(self):
        tab = ttk.Frame(self.tabs)
        tab.pack(fill='both', expand=1)
        self.tabs.add(tab, text="Перекодировать файлы")
        tk_recoder.tab_files_converter.init_frame(self, tab)

    def __init_tab3(self):
        tab = ttk.Frame(self.tabs)
        tab.pack(fill='both', expand=1)
        self.tabs.add(tab, text="Убрать BOM")
        tk_recoder.tab_bom_remover.init_frame(self, tab)

    # О программе
    def __init_tab4(self):
        tab = ttk.Frame(self.tabs)
        tab.pack(fill='both', expand=1)
        self.tabs.add(tab, text="О программе")
        tk_recoder.tab_about.init_frame(self, tab)
