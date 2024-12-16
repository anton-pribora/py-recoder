from recoder import Recoder
import os
import fnmatch


class Cli:
    def __init__(self, recorder: Recoder, config, arguments):
        super().__init__()
        self.recoder = recorder
        self.config = config
        self.arguments = arguments

    def run(self):
        if self.arguments.command == 'fc':
            self.convert_files()

    def update_status(self, text):
        print(text)

    def convert_files(self):
        """Поиск файлов в каталоге и его подкаталогах по маске"""
        current_list = list()
        mask = self.arguments.mask
        recursively = self.arguments.recursive

        def add_path(fullpath):
            if fullpath not in current_list:
                current_list.append(fullpath)

        def search(folder):
            if recursively:
                for root, dirs, files in os.walk(folder, topdown=False):
                    for name in files:
                        if mask == '' or fnmatch.fnmatch(name, mask):
                            path = os.path.join(root, name)
                            add_path(path)
            else:
                for item in os.listdir(folder):
                    path = os.path.join(folder, item)

                    if os.path.isfile(path) and (mask == '' or fnmatch.fnmatch(item, mask)):
                        add_path(path)

        for file in self.arguments.file:
            if os.path.isdir(file):
                search(file)
            else:
                add_path(file)

        if self.arguments.dry_run:
            for file in current_list:
                print(file)
            return

        def on_progress(text):
            self.update_status(text)
            return True

        for file in current_list:
            success, error = self.recoder.convert_file(
                enc_from=self.arguments.enc_from,
                enc_to=self.arguments.enc_to,
                file_path=file,
                save_origin=self.arguments.no_backup == False,
                origin_ext=self.arguments.backup_ext,
                progress_callback=on_progress
            )
            print('{file}: {result}'.format(file=file, result='успех' if success else error))