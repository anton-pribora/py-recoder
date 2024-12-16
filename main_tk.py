import os.path
import sys

from recoder import Recoder
from tk_recoder import gui, cli
import config
import args

arguments = args.parser.parse_args(sys.argv[1:])

config.load()
init_config = config.to_string()

log_file = os.path.join(config.application_path, f'{config.application_name}.log')
recoder = Recoder(config.config, log_file)

if arguments.command is not None:
    cli = cli.Cli(recoder, config, arguments)
    cli.run()
else:
    gui = gui.Gui(recoder, config.config)


    def on_close():
        current_config = config.to_string()

        if current_config != init_config:
            config.save()

        gui.destroy()


    gui.protocol('WM_DELETE_WINDOW', on_close)
    gui.mainloop()
