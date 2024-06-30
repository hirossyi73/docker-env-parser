from abc import ABC, abstractmethod


class ParserBase(ABC):
    """Parser Base Class"""
    from models.config import Config

    config: Config
    key: str

    def __init__(self,  config: Config, key: str):
        self.config = config
        self.key = key

    @abstractmethod
    def parse(self, content: str) -> str:
        pass

    @property
    def template_key(self) -> str:
        return '{{' + self.key + '}}'
