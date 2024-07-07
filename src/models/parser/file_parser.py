import os
from typing import Optional

from models.parser.parser_base import ParserBase


class FileParser(ParserBase):
    """File Parser. (Get from file)"""
    file_path: str
    folder_path: str
    value: Optional[str]

    from models.config import Config

    def __init__(self, config: Config, key: str, file_path: str):
        super().__init__(config, key)
        self.file_path = file_path
        self.value = None
        self.folder_path = os.path.dirname(file_path)

    def parse(self, content: str) -> str:
        # If value is already set, return it
        if self.value is not None:
            return self.value

        # Read file and set value
        path = f"{self.file_path}"
        with open(path, 'r') as f:
            self.value = f.read()

        return content.replace(self.template_key, self.value)
