import os


def get_item_path(root: str, item: str) -> str:
    _founded = False
    _path = root
    _subfolders = []
    while not _founded:
        for _item in os.listdir(_path):
            if _item[_item.find("%") + 1:] == item:
                _path = os.path.join(_path, _item)
                _founded = True
            elif os.path.isdir(f"{_path}/{_item}"):
                _subfolders.append(f"{_path}/{_item}")

        if not _founded:
            for folder in _subfolders:
                get_item_path(f"{_path}/{folder}", item)

    return _path if _founded else None
