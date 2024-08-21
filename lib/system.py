import os


def get_item_path(root: str, item: str) -> str:
    _founded = False
    _path = root
    _subfolders = []

    while not _founded:
        if not os.path.isdir(_path):
            _path = os.sep.join(_path.split(os.sep)[:-1])

        for _item in os.listdir(_path):
            if _item[_item.find("%") + 1:] == item:
                _path = os.path.join(_path, _item)
                _founded = True
                break
            elif os.path.isdir(f"{_path}{os.sep}{_item}"):
                _subfolders.append(_item)

        if not _founded:
            for folder in _subfolders:
                print(_subfolders)
                get_item_path(f"{_path}{os.sep}{folder}", item)
            if not _founded:
                break

    return _path if _founded else None
