import os
import shutil
import traceback
import uuid
from datetime import datetime


class Recoder:
    # Список кодировок для текста (заменяется списком из настроек)
    text_encodings = (
        'UTF-8',
        'windows-1251',
        'koi8-r',
        'cp866',
        'ISO 8859-5'
    )

    # Список кодировок для файлов (заменяется списком из настроек)
    file_encodings = (
        'UTF-8',
        'UTF-8 (BOM)',
        'windows-1251',
        'koi8-r',
        'cp866',
        'ISO 8859-5'
    )

    utf8_bom = b'\xEF\xBB\xBF'
    utf8_bom_encoding = 'UTF-8 (BOM)'
    utf8_encoding = 'UTF-8'

    def __init__(self, config, log_file):
        self.log_file = log_file
        self.config = config['recoder']
        self.text_encodings = tuple([x.strip() for x in self.config['text_encodings'].split(',') if x.strip()])
        self.file_encodings = tuple([x.strip() for x in self.config['file_encodings'].split(',') if x.strip()])

    @staticmethod
    def get_version():
        """
        Возвращает версию кодировщика

        :returns: текущая версия перекодировщика
        """
        return 'Recoder v3.1.0'

    def convert_text(self, enc_from, enc_to, text):
        """
        Переводит текст из одной кодировки в другую

        :arg enc_from: Кодировка исходного текста
        :arg enc_to: Кодировка, в которую нужно перевести текс
        :arg text: Исходный текст
        :return: result
        """
        data = bytes(text, enc_from, 'replace')

        if enc_to == self.utf8_bom_encoding:
            return str(data, 'utf-8-sig', 'replace')

        return str(data, enc_to, 'replace')

    def log(self, text):
        """
        Запись данных в лог работы программы

        :param text: Данные для лога
        :return:
        """
        with open(self.log_file, 'at', encoding='utf-8', errors='replace', newline='') as log:
            log.write(text + os.linesep)

    def convert_file(self, enc_from, enc_to, file_path, save_origin, origin_ext, progress_callback):
        """
        Перекодирует файл построчно

        :param enc_from: Исходная кодировка файла
        :param enc_to: Конечная кодировка файла
        :param file_path: Путь к файлу
        :param save_origin: Нужно ли сохранять оригинал
        :param origin_ext: Расширение для оригинального файла
        :param progress_callback: Хук для обработки прогресса
        :return: (True, None) если не было ошибок; (False, Error) если была ошибка
        """
        log = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            f'{enc_from} → {enc_to}',
            file_path
        ]

        result = True
        error = None

        # Если исходная кодировка UTF-8, то заменяем её на UTF8 с BOM, иначе маркер будет копироваться куда не надо
        # Результирующую кодировку также подменяем, если указана UTF-8 (BOM)
        source_encoding = 'utf-8-sig' if enc_from == self.utf8_encoding else enc_from
        result_encoding = 'utf-8-sig' if enc_to == self.utf8_bom_encoding else enc_to

        file_size = os.path.getsize(file_path)

        try:
            if file_size > int(self.config['big_file_size']):
                # Перекодировка больших файлов по следующей схеме:
                # 1. Создаём копию во временный файл
                # 2. Открываем исходный файл на запись
                # 3. Копируем построчно содержимое из копии в исходный файл с перекодировкой
                # 4. Если нужно сохранять оригинал, переименовываем временный файл, если нет - удаляем временный файл
                # 5. Перед копированием и на каждую 1000 перекодированных строк
                # 6. Если во время обработки пользователь прервёт операцию, восстановить исходный файл из временного

                temporary_file = file_path + '.tmp.' + str(uuid.uuid4())[0:3]
                progress_callback('Обработка {file}: создание временной копии'.format(file=file_path))
                shutil.copy2(file_path, temporary_file)

                with open(file_path, 'wt', encoding=result_encoding, errors='replace', newline='') as source:
                    with open(temporary_file, 'rt', encoding=source_encoding, errors='replace', newline='') as temp:
                        progress_callback('Обработка {file}: 0.0%'.format(file=file_path))

                        i = 0

                        while line := temp.readline():
                            source.write(line)

                            if i % int(self.config['big_file_lines_chunk']) == 0:
                                working = progress_callback('Обработка {file}: {percent:.1%}'.format(
                                    file=file_path,
                                    percent=temp.tell() / file_size
                                ))

                                if not working:
                                    # Обработка файла была прервана
                                    progress_callback('Обработка {file}: восстановление из временного файла'.format(
                                        file=file_path))
                                    source.close()
                                    temp.close()
                                    shutil.copy2(temporary_file, file_path)
                                    os.remove(temporary_file)
                                    raise Exception('Обработка была прервана')

                            i += 1

                source.close()
                temp.close()

                if save_origin:
                    os.rename(temporary_file, file_path + (origin_ext or '.orig'))
                else:
                    os.remove(temporary_file)
            else:
                # Перекодируем маленькие файлы по следующей схеме:
                # 1. Если нужно, сохраняем оригинал в отдельный файл
                # 2. Загружаем оригинал в память в исходной кодировке
                # 3. Обнуляем файл
                # 4. Сохраняем файл в нужной кодировке

                if save_origin:
                    shutil.copy2(file_path, file_path + (origin_ext or '.orig'))

                with open(file_path, 'r', encoding=source_encoding, errors='replace', newline='') as fp:
                    text = fp.read()
                    fp.close()

                with open(file_path, 'w', encoding=result_encoding, errors='replace', newline='') as fp:
                    fp.write(text)
                    fp.close()

            log.append('success')

        except Exception as e:
            traceback.print_exc()
            result = False
            error = e
            log.append('fail')
            log.append(str(e))

        self.log('\t'.join(log))
        return result, error

    def file_has_bom(self, path):
        """
        Проверяет, есть ли у файла BOM-заголовок

        :param path: Путь к файлу
        :return: True если заголовок есть, Fail если заголовка нет
        """
        with open(path, 'rb') as fp:
            return fp.read(len(self.utf8_bom)) == self.utf8_bom

    def remove_bom(self, file_path, progress_callback):
        """
        Убирает из файла заголовок BOM

        :param file_path: Путь к файлу
        :param progress_callback: Хук для обработки прогресса
        :return: (True, None) если не было ошибок; (False, Error) если была ошибка
        """
        return self.convert_file(self.utf8_encoding, self.utf8_encoding, file_path, False, '', progress_callback)