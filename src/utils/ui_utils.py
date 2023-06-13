import os

def _get_uis_directory() -> str:
    return os.path.abspath(os.path.join(__file__, '../../uis'))

def get_ui_file(file_name: str) -> str:
    return os.path.join(_get_uis_directory(), file_name)

def get_icon_file(file_name: str) -> str:
    return os.path.join(_get_uis_directory(), 'icons', file_name)
