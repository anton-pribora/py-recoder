import os.path

from recoder import Recoder
from tk_recoder import gui
import config

config.load()
init_config = config.to_string()

log_file = os.path.join(config.application_path, f'{config.application_name}.log')

recoder = Recoder(config.config, log_file)
gui = gui.Gui(recoder, config.config)


def on_close():
    current_config = config.to_string()

    if current_config != init_config:
        config.save()

    gui.destroy()


gui.protocol('WM_DELETE_WINDOW', on_close)
gui.mainloop()
