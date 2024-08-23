import os
from lib.blog.section import Section
from lib.blog.subsection import Subsection
from lib.blog.subsubsection import Subsubsection
from lib.utils.data.database import Database


class Mapper:
    _instance = None
    _content_folder = None
    _site_map = None
    _database = Database()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Mapper, cls).__new__(cls)
        return cls._instance

    def generate_site_map(self, content_folder: str):
        self._content_folder = content_folder
        self._site_map = self._generate_folder_map(folder_path=self._content_folder, parent=None)
        print(self._database.print())
        return self

    def _generate_folder_map(self, folder_path: str, parent) -> dict:
        record = None

        folder_map = {}
        folder_name = folder_path.split(os.sep)[-1]

        if folder_name != self._content_folder:
            folder_name = folder_name.split("%")[1]
            if parent is None:
                record = Section()
            elif type(parent) is Section:
                record = Subsection()
                record.section = parent.path
            elif type(parent) is Subsection:
                record = Subsubsection()
                record.section = parent.section
                record.subsection = parent.path

            record.title = folder_name
            record.path = folder_path
            self._database.create_record(record)

        folder_content = os.listdir(folder_path)

        # PYTHON 3.7+ DICT PRESERVE INSERTION ORDER. IF SOMETHING CHANGES ITEMS ORDER CAN BE COMPROMISED.
        folder_content.sort()

        # SEARCHING FOR DESCRIPTION FILE
        description = None
        description_path = folder_path + os.sep + "description"
        if os.path.exists(description_path):
            folder_content.remove("description")
            with open(description_path, "r") as f:
                description = f.read()

        subfolders = []
        md_files = []

        # ITERATING THROW THE FOLDER CONTENT
        for item in folder_content:
            if not item.startswith("%"):  # USED TO EXCLUDE A FOLDER FROM MAPPING
                if os.path.isdir(folder_path + os.sep + item):
                    subfolders.append(folder_path + os.sep + item)
                elif item.endswith(".md"):
                    md_files.append(item)

        temp = {}
        if folder_path != self._content_folder:
            post_map = {}
            for file in md_files:
                title = file.split("%")[1].replace(".md", "")
                post_map[title] = {"path": folder_path + os.sep + file}
            temp["posts"] = post_map
        if description is not None:
            temp["description"] = description

        temp["path"] = folder_path
        for subfolder in subfolders:
            temp["subfolders"] = self._generate_folder_map(subfolder, record)

        folder_map[folder_name] = temp

        return folder_map

    @property
    def site_map(self):
        return self._site_map
