from models.parser.custom_parser import ParserBase


class ConfigParser(ParserBase):
    """Config Parser. (Get from yml config)"""
    value: str

    from models.config import Config

    def __init__(self, config: Config, key: str, value: str):
        super().__init__(config, key)
        self.value = value

    def parse(self, content: str) -> str:
        return content.replace(self.template_key, self.value)
