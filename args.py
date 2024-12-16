import argparse
from recoder import Recoder


parser = argparse.ArgumentParser(
    epilog='(c) Anton Pribora 2024. Программа может нанести НЕОБРАТИМЫЙ ВРЕД вашим файлам. Используйте её с осторожностью.'
)

subparsers = parser.add_subparsers(
    title='Возможные команды',
    dest='command',
    description='Команды, которые должны быть в качестве первого параметра'
)

converter = subparsers.add_parser('fc', help='Конвертер файлов')

converter.add_argument('file', type=str, nargs='+', help='Файл или путь поиска')
converter.add_argument('-m', '--mask', type=str, default='*.*', help='Маска поиска')
converter.add_argument('-d', '--dry-run', action='store_true', default=False, help='Не выполнять конвертирование, просто вывести список файлов')
converter.add_argument('-r', '--recursive', action='store_true', default=False, help='Поиск в подкаталогах')
converter.add_argument('-n', '--no-backup', action='store_true', default=False, help='Отключить резервное копирование оригинала файла')
converter.add_argument('-e', '--backup-ext', type=str, default='.bak', help='Расширение оригинала')
converter.add_argument('-f', '--enc-from', type=str, required=True, help='Исходная кодировка', choices=Recoder.file_encodings)
converter.add_argument('-t', '--enc-to', type=str, required=True, help='Конечная кодировка', choices=Recoder.file_encodings)