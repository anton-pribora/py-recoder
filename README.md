# Recoder v3
Небольшая программа для массового (пакетного) перекодирования файлов из одной кодировки в другую.

[Основная страница программы](https://anton-pribora.ru/recoder/)

![Перекодировка текста](screenshots/recoder3_tab_tc.png)

![Перекодировка файлов](screenshots/recoder3_tab_fc.png)

## Установка

## Компиляция

Для сборки проекта в исполняемый файл перейдите в директорию проекта и выполните:

```bash
./venv/bin/pyinstaller -F -n recoder main_tk.py --collect-all tkinterdnd2
```