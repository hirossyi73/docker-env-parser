from __future__ import annotations
import os
from typing import Optional
import yaml


class Config:
    """Class that holds the contents of the configuration file"""
    _replacements: Optional[dict[str, str]]
    _is_ignore: Optional[bool]
    _is_auto_merge_config: Optional[bool]
    _is_only_replace_temp: Optional[bool]
    _is_multi_project_mode: Optional[bool]
    _replacement_files: Optional[dict[str, str]]
    _ignore_files: Optional[list[str]]
    _parsers: Optional[dict]

    def __init__(self):
        self._replacements = {}
        self._is_ignore = None
        self._is_auto_merge_config = None
        self._is_only_replace_temp = None
        self._is_multi_project_mode = None
        self._replacement_files = None
        self._ignore_files = None
        self._parsers = None

    @property
    def replacements(self) -> dict[str, str]:
        """Dictionary for parameter replacements"""
        return self._replacements if self._replacements is not None else {}

    @property
    def is_ignore(self) -> bool:
        """Whether to ignore globally or not"""
        return self._is_ignore if self._is_ignore is not None else False

    @property
    def is_auto_merge_config(self) -> bool:
        """Whether to automatically merge configuration files or not"""
        return self._is_auto_merge_config if self._is_auto_merge_config is not None else True

    @property
    def is_only_replace_temp(self) -> bool:
        """Whether to only replace ".temp" files or not"""
        return self._is_only_replace_temp if self._is_only_replace_temp is not None else False

    @property
    def is_multi_project_mode(self) -> bool:
        """Whether to use multi-project mode or not"""
        return self._is_multi_project_mode if self._is_multi_project_mode is not None else False

    @property
    def replacement_files(self) -> dict[str, str]:
        """List of files to perform replacements on"""
        return self._replacement_files if self._replacement_files is not None else {}

    @property
    def ignore_files(self) -> list[str]:
        """List of files to ignore for replacements"""
        return self._ignore_files if self._ignore_files is not None else []

    def init_config(self, root_path: str | None, environment: str, global_config: Config = None) -> dict:
        """Reads the configuration file and sets the parameters"""
        config_dict = {}
        base_path = (root_path if root_path is not None else '') + ('/' if root_path is not None else '')

        # Read the common configuration file if it exists
        path = f'{base_path}config.yml'
        _config_dict = self._get_config_dict_from_path(path)
        config_dict = self._merge_config_dict(_config_dict, config_dict)

        # Read the environment-specific configuration file if it exists
        if environment is not None:
            path = f'{base_path}config.{environment}.yml'
            _config_dict = self._get_config_dict_from_path(path)
            config_dict = self._merge_config_dict(_config_dict, config_dict)

        # Set the parameters
        self._set_config_from_dict(config_dict, base_path, global_config)

        return config_dict

    def get_parsers(self) -> dict:
        """Get parsers (config, file, custom)"""
        # Return as it is if already obtained
        if self._parsers is not None:
            return self._parsers

        from models.parser.param_parser import ParamParser
        from models.parser.file_parser import FileParser
        parsers = {}

        # Get parser from config
        for key, value in self.replacements.items():
            parsers[key] = ParamParser(self, key, value)

        # Get file parser
        for key, path in self.replacement_files.items():
            parsers[key] = FileParser(self, key, path)

        self._parsers = parsers
        return self._parsers

    def _set_config_from_dict(self, config_dict: dict, base_path: str, global_config: Config = None):
        """Set the parameters from the dictionary"""

        # Set the parameters
        self._replacements = self._get_config_value(config_dict, ['replacements'])
        self._is_ignore = self._get_config_value(config_dict, ['settings', 'is_ignore'])
        self._is_auto_merge_config = self._get_config_value(config_dict, ['settings', 'is_auto_merge_config'])
        self._is_only_replace_temp = self._get_config_value(config_dict, ['settings', 'is_only_replace_temp'])
        self._is_multi_project_mode = self._get_config_value(config_dict, ['settings', 'is_multi_project_mode'])
        self._ignore_files = self._get_config_value(config_dict, ['settings', 'ignore_files'])
        self._replacement_files = self._get_replacement_files(base_path)

        # Merge global config and config
        if global_config is not None:
            self._is_ignore = global_config.is_ignore if self._is_ignore is None else self.is_ignore
            self._is_auto_merge_config = global_config.is_auto_merge_config if self._is_auto_merge_config is None else self.is_auto_merge_config
            self._is_only_replace_temp = global_config.is_only_replace_temp if self._is_only_replace_temp is None else self.is_only_replace_temp
            self._is_multi_project_mode = global_config.is_multi_project_mode if self._is_multi_project_mode is None else self.is_multi_project_mode

            # Append Items
            self._replacements = {**global_config.replacements, **self.replacements}
            self._replacement_files = {**global_config.replacement_files, **self.replacement_files}
            self._ignore_files = global_config.ignore_files + self.ignore_files

    def _merge_config_dict(self, config_dict: dict, base_config_dict: dict) -> dict:
        """Merge values from the configuration file"""
        merged_config = {**({} if base_config_dict is None else base_config_dict),
                         **({} if config_dict is None else config_dict)}
        return merged_config

    def _get_config_dict_from_path(self, path: str) -> dict:
        yaml_string = self._read_string_from_path(path)
        return self._get_config_dict_from_yaml(yaml_string)

    def _read_string_from_path(self, path: str) -> str:
        """Read a file as a string"""
        if not os.path.isfile(path):
            return None
        with open(path, encoding='utf-8')as f:
            return f.read()

    def _get_config_value(self, config: dict, keys: list[str]):
        """Get the value from the configuration file"""
        if config is None:
            return None
        else:
            vals = config
            for key in keys:
                if key not in vals:
                    return None
                    break
                vals = vals[key]
        return vals

    def _get_config_dict_from_yaml(self, yaml_string: str) -> dict:
        """get yaml values from a YAML string"""
        if yaml_string is None:
            return {}
        r = yaml.safe_load(yaml_string)
        # Merge if the value exists
        if r is None:
            return {}
        return r

    def _get_replacement_files(self, base_path: str) -> dict[str, str]:
        """Get the list of files for replacements"""
        result = {}
        replacement_files_path = f'{base_path}replacement_files'
        if not os.path.exists(replacement_files_path):
            return result
        files = os.listdir(replacement_files_path)
        for file in files:
            # Set the file name (without extension) as the key and base_path + file as the value
            result[os.path.basename(file)] = f'{base_path}replacement_files/{file}'
        return result


class GlobalConfig(Config):
    """Class that holds the contents of the configuration file (for all environments)"""
    _environments: list[str]

    def __init__(self):
        super().__init__()
        self._environments = []

    @property
    def environments(self) -> list[str]:
        return self._environments

    def init_config(self, root_path: str | None, environment: str):
        """Reads the configuration file and sets the parameters"""
        config = super().init_config(root_path, environment)

        # Set the parameters
        self._environments = self._get_config_value(config, ['environments'])
        if self._environments is None:
            raise Exception('environments is not found in config.yml')

        return config
