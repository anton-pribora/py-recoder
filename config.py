import configparser
import sys
import os
from pathlib import Path

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_name = Path(sys.executable).stem
    application_path = os.path.dirname(sys.executable)
else:
    application_name = Path(sys.argv[0]).stem
    application_path = os.path.dirname(__file__)

config = configparser.ConfigParser()
config_file = f'{application_path}/{application_name}.ini'

config['recoder'] = {
    'text_encodings': 'UTF-8, windows-1251, koi8-r, cp866, ISO 8859-5',
    'file_encodings': 'UTF-8, UTF-8 (BOM), windows-1251, koi8-r, cp866, ISO 8859-5',
    'big_file_size': 1024 * 1024,
    'big_file_lines_chunk': 1000
}

config['text_converter'] = {
    'enc_from': 'windows-1251',
    'enc_to': 'UTF-8'
}

config['files_converter'] = {
    'path': application_path,
    'mask': '*.txt',
    'enc_from': 'windows-1251',
    'enc_to': 'UTF-8',
    'save_origin': True,
    'origin_ext': '~'
}

config['bom_remover'] = {
    'path': application_path,
    'mask': '*.*'
}


def load():
    config.read(config_file)


def save():
    with open(config_file, 'w') as fp:
        config.write(fp)


def to_string():
    return str({section: dict(config[section]) for section in config.sections()})
