from typing import Optional

from models.parser.parser_base import ParserBase


class FileParser(ParserBase):
    """File Parser. (Get from file)"""
    path: str
    value: Optional[str]

    from models.config import Config

    def __init__(self, config: Config, key: str, path: str):
        super().__init__(config, key)
        self.path = path

    def parse(self, content: str) -> str:
        # If value is already set, return it
        if self.value is not None:
            return self.value

        # Read file and set value
        with open(self.path, 'r') as f:
            self.value = f.read()

        return content.replace(self.template_key, self.value)
