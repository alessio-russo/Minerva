class Section:

    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path