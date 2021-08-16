import os
import platform


def check_os():
    """
    Проверяем какая система Linux или Windows, такие будут и пути
    """
    dir_src = os.path.abspath(os.curdir)
    if platform.system() == "Windows":
        return fr"{dir_src}\json\db", fr"{dir_src}\json\admin"
    elif platform.system() == "Linux":
        return f"{dir_src}/json/db", f"{dir_src}/json/admin"
    else:
        print("Этот скрипт не поддерживает MacOS")