import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, DEFAULTS

FILE_SET = UploadSet("files", DEFAULTS) 


def save_file(file: FileStorage, folder: str = None, name: str = None) -> str:
    return FILE_SET.save(file, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    return FILE_SET.path(filename, folder)


def find_file_any_format(filename: str, folder: str) -> Union[str, None]:

    for _format in DEFAULTS: 
        avatar = f"{filename}.{_format}"
        avatar_path = FILE_SET.path(filename=avatar, folder=folder)
        if os.path.isfile(avatar_path):
            return avatar_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:

    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:

    filename = _retrieve_filename(file)

    allowed_format = "|".join(DEFAULTS)

    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:

    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
