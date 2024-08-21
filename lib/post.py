import os
import time
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
from pygments.formatters import HtmlFormatter
from datetime import datetime


class Post:
    def __init__(self, filename: str):
        self._filename = filename

    def get_content(self):
        with open(self._filename, "r") as file:
            md_content = markdown.markdown(file.read(), extensions=["fenced_code", "codehilite", 'mdx_math'],
                                                   extension_configs={
                                                       'mdx-math': {'enable_dollar_delimiter': True}})

        formatter = HtmlFormatter(style="friendly", full=True, cssclass="codehilite")
        css = formatter.get_style_defs()
        md_css_string = "<style>" + css + "</style>"

        return md_css_string + md_content

    def get_m_time(self) -> datetime:
        data = os.path.getmtime(self._filename)
        data = time.ctime(data)
        data = datetime.strptime(data, "%a %b %d %H:%M:%S %Y")
        return data

    def get_title(self) -> str:
        filename = self._filename.split("/")[-1].replace(".md", "")
        return filename[filename.find('.')+1:].capitalize()