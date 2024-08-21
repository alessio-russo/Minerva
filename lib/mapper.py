import os
import json
import lib.system as system


class Mapper:

    def __init__(self, content_folder: str):
        self._content_folder = content_folder
        self._site_map = self._generate_site_map()

    def _generate_site_map(self):
        site_map = "{"
        site_map += self._generate_folder_map(self._content_folder)
        site_map += "}"
        return json.loads(site_map)

    def _generate_folder_map(self, path: str):

        # FOLDER PREPROCESSING
        parent = path.split(os.sep)[-1]
        parent = parent[parent.find("%") + 1:]
        parent = parent.lower()

        folder_map = "," if path != self._content_folder else ""
        folder_map += f"\"{parent}\": " + "{ "

        folder = os.listdir(path)
        folder.sort()

        # SEARCHING FOR DESCRIPTION FILE
        description = None
        if os.path.exists(f"{path}/description"):
            folder.remove("description")
            with open(f"{path}/description", "r") as f:
                description = f.read()

        subfolders = []
        md_files = []

        # ITERATING THROW THE FOLDER
        for item in folder:
            if not item.startswith("%"):  # USED TO EXCLUDE A FOLDER FROM MAPPING

                item = item.split("%")[1]
                path = system.get_item_path(root=path, item=item)

                if path is not None:
                    if os.path.isdir(path):
                        subfolders.append(path)
                    elif item.endswith(".md"):
                        md_files.append(item)

        # ITERATING THROW THE MD FILES
        if len(md_files) > 0:
            folder_map += " \"posts\" : ["
            for i, file in enumerate(md_files):
                file = file.replace('.md', '')
                file = file.lower()

                folder_map += f"\"{file}\""

                if i != len(md_files) - 1:
                    folder_map += ","
            folder_map += "] "

        # ITERATING THROW THE FOLDERS
        if len(subfolders) > 0:
            if len(md_files) > 0:
                folder_map += " , "
            folder_map += "\"folders\" : ["
            for i, folder in enumerate(subfolders):
                folder = folder.lower()
                folder = folder.split(os.sep)[-1].split("%")[1]
                folder_map += f"\"{folder}\""

                if i != len(subfolders) - 1:
                    folder_map += ","
            folder_map += "] "

        # READING DESCRIPTION
        if description is not None:
            if len(subfolders) > 0 or len(md_files) > 0:
                folder_map += ", "
            folder_map += "\"description\":"
            folder_map += f"\"{description}\""

        folder_map += "} "
        for folder in subfolders:
            folder_map += self._generate_folder_map(folder)

        return folder_map

    def get_site_map(self):
        return self._site_map
