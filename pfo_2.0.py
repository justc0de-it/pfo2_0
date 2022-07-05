# Импорт необходимых библиотек
import locale
import os
import shutil

from dotenv import dotenv_values
from rich.console import Console
from rich.progress import track
from art import *

# Определяем консоль для вывода красивых сообщений
console = Console()

# Определяем язык системы
sys_lang = locale.getdefaultlocale()


# Получаем названия пользовательских директорий
def get_user_dir(name: str) -> str:
    # Сперва получаем домашний каталог традиционным способом
    home_dir = os.path.expanduser("~")

    # Потом ищем путь к каталогу, в котором хранятся настройки
    config_dir = os.getenv("XDG_CONFIG_HOME") or os.path.join(home_dir, ".config")

    # Загружаем файл с описанием каталогов
    data = dotenv_values(os.path.join(config_dir, "user-dirs.dirs"))

    # Получаем путь из файла или генерируем его, если в файле нет нужного пути
    key = f"XDG_{name}_DIR"
    if key in data:
        path = data[key]
    elif key == "DESKTOP":
        path = os.path.join(home_dir, "Desktop")
    else:
        path = home_dir

    # Если путь начинается на $HOME, то нужно подставить туда домашний каталог
    if path.startswith("$HOME/"):
        path = os.path.join(home_dir, path[6:])

    return path


# Получаем список файлов в папке с загрузками
file_list = os.listdir(get_user_dir("DOWNLOAD"))

# Создаём списки с файлами
video_ext = [".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".wmv", ".webm"]
pictures_ext = [".raw", ".jpg", ".tiff", ".psd", ".bmp", ".gif", ".png", ".jp2", ".jpeg"]
docs_ext = [".doc", ".docx", ".odt", ".txt", ".rtf", ".pdf", ".fb2", ".djvu",
            ".xls", ".xlsx", ".ppt", ".pptx",
            ".mdb", ".accdb", ".rar", ".zip", ".7z"]
music_ext = [".mp3", ".aac", ".flac", ".mpc", ".wma", ".wav"]


# Функции перемещения и удаления файлов после перемещения
def move_video(file_ext, downloads_folder):
    for ext in file_ext:
        for file in downloads_folder:
            if file.endswith(ext) and os.path.isfile(get_user_dir("DOWNLOAD") + "/" + file):
                shutil.move(get_user_dir("DOWNLOAD") + "/" + file, get_user_dir("VIDEOS") + "/" + file)


def move_pictures(file_ext, downloads_folder):
    for ext in file_ext:
        for file in downloads_folder:
            if file.endswith(ext) and os.path.isfile(get_user_dir("DOWNLOAD") + "/" + file):
                shutil.move(get_user_dir("DOWNLOAD") + "/" + file, get_user_dir("PICTURES") + "/" + file)


def move_music(file_ext, downloads_folder):
    for ext in file_ext:
        for file in downloads_folder:
            if file.endswith(ext) and os.path.isfile(get_user_dir("DOWNLOAD") + "/" + file):
                shutil.move(get_user_dir("DOWNLOAD") + "/" + file, get_user_dir("MUSIC") + "/" + file)


def move_docs(file_ext, downloads_folder):
    for ext in file_ext:
        for file in downloads_folder:
            if file.endswith(ext) and os.path.isfile(get_user_dir("DOWNLOAD") + "/" + file):
                shutil.move(get_user_dir("DOWNLOAD") + "/" + file, get_user_dir("DOCUMENTS") + "/" + file)


def delete_files():
    for file_to_remove in file_list:
        if os.path.exists(get_user_dir("DOWNLOAD")) and os.path.isfile(get_user_dir("DOWNLOAD") + "/" + file_to_remove):
            os.remove(get_user_dir("DOWNLOAD") + "/" + file_to_remove)


def what_next():
    count = 0
    for remaining_files in os.listdir(get_user_dir("DOWNLOAD")):
        if os.path.isfile(os.path.join(get_user_dir("DOWNLOAD"), remaining_files)):
            count += 1
        if count > 0:
            # Спрашиваем пользователя о дальнейших действиях
            next_msg = console.input(next_msg_text) or "1"
            if next_msg == "2":
                # Удаляем файлы
                for _ in track(range(100), description=delete_progress_text):
                    delete_files()


if __name__ == '__main__':
    # Выводим красивое название программы
    start_msg = text2art("PFO 2.0")
    print(start_msg)
    # Выводим стартовое сообщение
    if "ru_RU" in sys_lang:
        console.input("[bold green]Введите название папки с загрузками (Загрузки): ") or get_user_dir("DOWNLOAD")
    else:
        console.input("[bold green]Enter the name of the downloads folder (Downloads): ") or get_user_dir("DOWNLOAD")
    # Определяем язык статус-бара прогресса
    if "ru_RU" in sys_lang:
        progress_text = "[bold blue]Перемещаем файлы"
        delete_progress_text = "[bold red]Удаляем файлы"
        next_msg_text = "[bold violet]Удалить оставшиеся файлы? 1 - нет, 2 - да (1): "
        finish_msg_text = "Программа завершила работу"
    else:
        progress_text = "[bold blue]Moving files"
        delete_progress_text = "[bold red]Delete files"
        next_msg_text = "[bold violet]Delete remaining files? 1 - no, 2 - yes (1): "
        finish_msg_text = "The program has ended"
    # Выводим статус-бар с прогрессом перемещения
    for _ in track(range(100), description=progress_text):
        move_video(video_ext, file_list)
        move_music(music_ext, file_list)
        move_pictures(pictures_ext, file_list)
        move_docs(docs_ext, file_list)
    # Определяем есть ли в директории оставшиеся файлы и если да, то спрашиваем пользователя что дальше
    what_next()
    console.print(finish_msg_text, style="bold green")
