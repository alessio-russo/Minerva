import os
import json


class Scanner:

    def __init__(self, content_dir: str):
        self._root = f"{os.getcwd()}/{content_dir}"

    def _scan(self, path:str):
        parent = path.split("/")[-1]
        parent = parent.replace(' ', '_')
        parent = parent.lower()
        result = f"\"{parent}\": "
        result += "{ \"dir\" : ["
        folder = os.listdir(path)
        try:
            folder.remove("description")
        except:
            pass
        subfolders = []

        for i, elem in enumerate(folder):
            if not elem.startswith("_"):

                if os.path.isdir(f"{path}/{elem}"):
                    subfolders.append(f"{path}/{elem}")

                elem = elem.replace(' ', '_')
                elem = elem.lower()

                result += f"\"{elem}\""

                if i != len(folder) - 1:
                    result += ","
        result += "]"
        try:
            with open(f"{path}/description", "r") as f:

                result += ", \"description\":"
                result += f"\"{f.read()}\""
                result += "}"
        except:
            result += "}"

        if len(subfolders) != 0:
            result += ","

            for i, dir in enumerate(subfolders):
                result += self._scan(dir)

                if i != len(subfolders) - 1:
                    result += ","

        return result

    def get_structure(self):
        content = "{"
        content += self._scan(self._root)
        content += "}"
        structure = json.loads(content)
        return structure
