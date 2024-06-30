from abc import abstractmethod
from typing import Optional

from models.parser.file_parser import ParserBase


class CustomParserOptions:
    """Custom Parser Options. (Maybe use for custom parser)"""

    def __init__(self):
        pass


class CustomParser(ParserBase):
    """Custom Parser. (Get from custom function)"""
    option: CustomParserOptions
    value: Optional[str]

    from models.config import Config

    def __init__(self, config: Config, key: str, option: CustomParserOptions):
        super().__init__(config, key)
        self.option = option

    @abstractmethod
    def parse(self, content: str) -> str:
        pass
