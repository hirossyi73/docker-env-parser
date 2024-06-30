from abc import ABC, abstractmethod

from models.config import Config


class ParserBase(ABC):
    def __init__(self,  config: Config):
        self.config = config

    @abstractmethod
    def parse(self, key: str, content: str) -> str:
        pass
