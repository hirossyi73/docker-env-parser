from __future__ import annotations
import os
from typing import Optional

import yaml


class Config:
    """ 設定ファイルの内容を保持するクラス """
    # パラメータ置き換え用の辞書
    _replacements: Optional[dict[str, str]]
    # プロジェクト全体で除外するかどうか
    _is_ignore: Optional[bool]
    # 自動的に設定ファイルのマージを行うかどうか
    _is_auto_merge_config: Optional[bool]
    # ".temp"ファイルのみ置き換えを行うかどうか
    _is_only_replace_temp: Optional[bool]
    # 複数プロジェクトモードを使用するかどうか
    _is_multi_project_mode: Optional[bool]
    # 置き換えを行うファイルの一覧
    _replacement_files: Optional[dict[str, str]]
    # 置き換えを実施しないファイルの一覧
    _ignore_files: Optional[list[str]]
    # パラメータ置き換えを行うためのパーサー
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
        return self._replacements if self._replacements is not None else {}

    @property
    def is_ignore(self) -> bool:
        return self._is_ignore if self._is_ignore is not None else False

    @property
    def is_auto_merge_config(self) -> bool:
        return self._is_auto_merge_config if self._is_auto_merge_config is not None else True

    @property
    def is_only_replace_temp(self) -> bool:
        return self._is_only_replace_temp if self._is_only_replace_temp is not None else False

    @property
    def is_multi_project_mode(self) -> bool:
        return self._is_multi_project_mode if self._is_multi_project_mode is not None else False

    @property
    def replacement_files(self) -> dict[str, str]:
        return self._replacement_files if self._replacement_files is not None else {}

    @property
    def ignore_files(self) -> list[str]:
        return self._ignore_files if self._ignore_files is not None else []

    def init_config(self, root_path: str | None, environment: str, global_config: Config = None) -> dict:
        """ 設定ファイルを読みこみでパラメータにセットする """
        config = {}
        base_path = (root_path if root_path is not None else '') + ('/' if root_path is not None else '')

        # 共通の設定ファイルが存在する場合、読み込む
        path = f'{base_path}config.yml'
        config = self._merge_config(path, config)

        # 環境用の設定ファイルが存在する場合、読み込む
        if environment is not None:
            path = f'{base_path}config.{environment}.yml'
            config = self._merge_config(path, config)

        # 各パラメータにセット
        self._replacements = self._get_config_value(config, ['replacements'])
        self._is_ignore = self._get_config_value(config, ['settings', 'is_ignore'])
        self._is_auto_merge_config = self._get_config_value(config, ['settings', 'is_auto_merge_config'])
        self._is_only_replace_temp = self._get_config_value(config, ['settings', 'is_only_replace_temp'])
        self._is_multi_project_mode = self._get_config_value(config, ['settings', 'is_multi_project_mode'])
        self._ignore_files = self._get_config_value(config, ['settings', 'ignore_files'])
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

        return config

    def get_parsers(self) -> dict:
        """ Get parsers(config, file, custom) """
        if self._parsers is not None:
            return self._parsers

        from models.parser.config_parser import ConfigParser
        from models.parser.file_parser import FileParser
        parsers = {}

        # get parser from config
        for key, value in self.replacements.items():
            parsers[key] = ConfigParser(self, key, value)

        # get file parser
        for key, path in self.replacement_files.items():
            parsers[key] = FileParser(self, key, path)

        self._parsers = parsers
        return self._parsers

    def _merge_config(self, path: str, config: dict) -> dict:
        """ 設定ファイルから値をマージする """
        config = Config.get_yaml_config(path)
        config = {**config, **({} if config is None else config)}
        return config

    def _get_config_value(self, config: dict, keys: list[str]):
        """ configから値を取得する処理 """
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

    def _get_replacement_files(self, base_path: str) -> dict[str, str]:
        """ ファイルによる変換のファイル名一覧を取得 """
        result = {}
        replacement_files_path = f'{base_path}replacement_files'
        if not os.path.exists(replacement_files_path):
            return result
        files = os.listdir(replacement_files_path)
        for file in files:
            # キー名にファイル名(拡張子は除く)、値にbase_path + fileをセット
            result[os.path.basename(file)] = f'{base_path}replacement_files/{file}'
        return result

    @staticmethod
    def get_yaml_config(path: str) -> dict:
        """ yamlファイルから値をマージする """
        if not os.path.isfile(path):
            return {}
        with open(path, encoding='utf-8')as f:
            r = yaml.safe_load(f)
            # 値が存在してれば、マージ
            if r is None:
                return {}
            return r


class GlobalConfig(Config):
    """ 設定ファイルの内容を保持するクラス(全環境用) """
    _environments: list[str]

    def __init__(self):
        super().__init__()
        self._environments = []

    @property
    def environments(self) -> list[str]:
        return self._environments

    def init_config(self, root_path: str | None, environment: str):
        """ 設定ファイルを読みこみでパラメータにセットする """
        config = super().init_config(root_path, environment)

        # パラメータにセット
        self._environments = self._get_config_value(config, ['environments'])
        if self._environments is None:
            raise Exception('environments is not found in config.yml')

        return config
