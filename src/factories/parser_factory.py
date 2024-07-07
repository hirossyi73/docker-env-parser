from abc import ABC, abstractmethod
import os
from models.const import FolderName
from models.parser.file_parser import FileParser
from models.parser.param_parser import ParamParser
from models.parser.parser_base import ParserBase


class ParserFactoryBase(ABC):
    """Abstract Factory for creating Parser instances"""

    from models.config import Config

    @abstractmethod
    def makes(self, config: Config) -> list[ParserBase]:
        pass


class ParserFactory(ParserFactoryBase):
    """Factory for creating Parser instances(default)"""

    from models.config import Config

    def makes(self, config: Config) -> dict[str, ParserBase]:
        result = {}

        ########## Define as param-parser ##########
        result.update(self._get_param_parsers(config))

        ########## Define as file-parser ##########
        result.update(self._get_file_parsers(config))

        return result

    def _get_param_parsers(self, config: Config) -> dict[str, ParamParser]:
        """Get the list of params for replacements
        key: key name
        value: replace value
        """
        result = {}

        for key, value in config.replacement_params.items():
            result[key] = ParamParser(config, key, value)

        return result

    def _get_file_parsers(self, config: Config) -> dict[str, FileParser]:
        """Get the list of files for replacements
        key: key name
        value: file path
        * If file name is such as "EXE_NAME.develop.yml", key is "EXE_NAME", and value is "path/to/EXE_NAME.develop.yml"
        """
        tmp_result = {}

        # get all files in the replacement_files directory
        files = config.replacement_files
        for file in files:
            # get only .txt files
            file_name = os.path.basename(file)
            if not file_name.endswith('.txt'):
                continue
            # Remove ".txt" name.
            base_name = file_name.replace('.txt', '')
            tmp_result[base_name] = f'{config.base_path}/{FolderName.REPLACEMENT_FILES.value}/{file}'

        # Re-loop result array. And if contains ".", check env in arg[1].
        # And if match arg[1], set as key: arg[0] value: arg[1]
        result = {}
        for key, path in tmp_result.items():
            if '.' not in key:
                result[key] = FileParser(self, key, path)
                continue

            # Check environment. If not match, skip.
            key_env = key.split('.')[1]
            if key_env != config.environment:
                continue
            # Set key without env.
            else:
                _key = key.split('.')[0]
                result[_key] = FileParser(config, _key, path)

        return result
