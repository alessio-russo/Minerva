import os
import json


class Scanner:

    def __init__(self, content_dir: str):
        self._root = content_dir

    def _scan(self, path: str):
        parent = path.split("/")[-1]
        parent = parent.replace(' ', '_')
        parent = parent.lower()

        result = "," if path != self._root else ""
        result += f"\"{parent}\": " + "{ "

        folder = os.listdir(path)

        try:
            folder.remove("description")
        except:
            pass

        subfolders = []
        files = []

        # ITERATING THROW THE FOLDER
        for elem in folder:
            if not elem.startswith("_"):
                if os.path.isdir(f"{path}/{elem}"):
                    subfolders.append(f"{path}/{elem}")
                else:
                    files.append(elem)

        # ITERATING THROW THE FILES
        if len(files) > 0:
            result += " \"files\" : ["
            for i, file in enumerate(files):
                file = file.replace(' ', '_')
                file = file.lower()

                result += f"\"{file}\""

                if i != len(files) - 1:
                    result += ","
            result += "] "

        # ITERATING THROW THE FOLDERS
        if len(subfolders) > 0:
            if len(files) > 0:
                result += " , "
            result += "\"dir\" : ["
            for i, folder in enumerate(subfolders):
                folder = folder.replace(' ', '_')
                folder = folder.lower()
                folder = folder.split('/')[-1]
                result += f"\"{folder}\""

                if i != len(subfolders) - 1:
                    result += ","
            result += "] "

        try:
            with open(f"{path}/description", "r") as f:
                if len(subfolders) > 0 or len(files) > 0:
                    result += ", "
                result += "\"description\":"
                result += f"\"{f.read()}\""

        except:
            pass
        result += "} "
        for folder in subfolders:
            result += self._scan(folder)

        return result

    def get_structure(self):
        content = "{"
        content += self._scan(self._root)
        content += "}"
        structure = json.loads(content)
        return structure
