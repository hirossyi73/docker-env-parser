from typing import Optional
from models.config import Config, GlobalConfig


class ConfigMock(Config):
    def set_replacements(self, replacements: Optional[dict[str, str]]) -> None:
        self._replacements = replacements

    def set_is_ignore(self, is_ignore: Optional[bool]) -> None:
        self._is_ignore = is_ignore

    def set_is_auto_merge_config(self, is_auto_merge_config: Optional[bool]) -> None:
        self._is_auto_merge_config = is_auto_merge_config

    def set_is_only_replace_temp(self, is_only_replace_temp: Optional[bool]) -> None:
        self._is_only_replace_temp = is_only_replace_temp

    def set_is_multi_project_mode(self, is_multi_project_mode: Optional[bool]) -> None:
        self._is_multi_project_mode = is_multi_project_mode

    def set_replacement_files(self, replacement_files: Optional[dict[str, str]]) -> None:
        self._replacement_files = replacement_files

    def set_ignore_files(self, ignore_files: Optional[list[str]]) -> None:
        self._ignore_files = ignore_files

    def set_parsers(self, parsers: Optional[dict]) -> None:
        self._parsers = parsers


class GlobalConfigMock(GlobalConfig):
    def set_replacements(self, replacements: Optional[dict[str, str]]) -> None:
        self._replacements = replacements

    def set_is_ignore(self, is_ignore: Optional[bool]) -> None:
        self._is_ignore = is_ignore

    def set_is_auto_merge_config(self, is_auto_merge_config: Optional[bool]) -> None:
        self._is_auto_merge_config = is_auto_merge_config

    def set_is_only_replace_temp(self, is_only_replace_temp: Optional[bool]) -> None:
        self._is_only_replace_temp = is_only_replace_temp

    def set_is_multi_project_mode(self, is_multi_project_mode: Optional[bool]) -> None:
        self._is_multi_project_mode = is_multi_project_mode

    def set_replacement_files(self, replacement_files: Optional[dict[str, str]]) -> None:
        self._replacement_files = replacement_files

    def set_ignore_files(self, ignore_files: Optional[list[str]]) -> None:
        self._ignore_files = ignore_files

    def set_parsers(self, parsers: Optional[dict]) -> None:
        self._parsers = parsers

