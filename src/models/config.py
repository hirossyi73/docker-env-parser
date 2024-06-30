from __future__ import annotations
from typing import Optional
from helpers.helper import Helper


class Config:
    """ 設定ファイルの内容を保持するクラス """
    # パラメータ置き換え用の辞書
    _replacements: Optional[dict]
    # プロジェクト全体で除外するかどうか
    _is_ignore: Optional[bool]
    # 自動的に設定ファイルのマージを行うかどうか
    _is_auto_merge_config: Optional[bool]
    # ".temp"ファイルのみ置き換えを行うかどうか
    _is_only_replace_temp: Optional[bool]
    # 複数プロジェクトモードを使用するかどうか
    _is_multi_project_mode: Optional[bool]
    # 置き換えを行うファイルの一覧
    _replace_files: Optional[list[str]]
    # 置き換えを実施しないファイルの一覧
    _ignore_files: Optional[list[str]]

    def __init__(self):
        self._replacements = {}
        self._is_ignore = None
        self._is_auto_merge_config = None
        self._is_only_replace_temp = None
        self._is_multi_project_mode = None
        self._ignore_files = None

    @property
    def replacements(self) -> dict:
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
    def ignore_files(self) -> list[str]:
        return self._ignore_files if self._ignore_files is not None else []

    def init_config(self, root_path: str | None, environment: str, global_config: Config = None) -> dict:
        """ 設定ファイルを読みこみでパラメータにセットする """
        config = {}

        # 共通の設定ファイルが存在する場合、読み込む
        base_path = (root_path if root_path is not None else '') + ('/' if root_path is not None else '')
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

        # Merge global config and config
        if global_config is not None:
            self._is_ignore = global_config.is_ignore if self._is_ignore is None else self.is_ignore
            self._is_auto_merge_config = global_config.is_auto_merge_config if self._is_auto_merge_config is None else self.is_auto_merge_config
            self._is_only_replace_temp = global_config.is_only_replace_temp if self._is_only_replace_temp is None else self.is_only_replace_temp
            self._is_multi_project_mode = global_config.is_multi_project_mode if self._is_multi_project_mode is None else self.is_multi_project_mode

            # Append Items
            self._replacements = {**global_config.replacements, **self.replacements}
            self._ignore_files = global_config.ignore_files + self.ignore_files

        return config

    def _merge_config(self, path: str, config: dict) -> dict:
        """ 設定ファイルから値をマージする """
        config = Helper.get_yaml_config(path)
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
