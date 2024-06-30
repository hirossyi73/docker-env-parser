
import fnmatch
import os
import shutil
from models.config import Config
import yaml


class Project:
    config: Config

    def __init__(self, name: str, config: Config):
        self.name = name
        self.config = config

    @property
    def pjroot(self):
        """ プロジェクトのルートパス """
        if self.config.is_multi_project_mode:
            return f"templates/{self.name}"
        return "templates"

    def get_pj_dist_root(self, environment: str):
        """ プロジェクトのdistのルートパスを取得 """
        if self.config.is_multi_project_mode:
            return f'dist/docker-{environment}/{self.name}'
        return f'dist/docker-{environment}'

    def build(self, environment: str):
        # 除外する設定の場合はスキップ
        if self.config.is_ignore:
            return

        # "temp"フォルダ内のファイル一覧を取得
        files = self._get_all_files(f"{self.pjroot}/src")
        for file in files:
            # "src/"までのパスを削除したファイル名取得
            file_rel_path = file.replace(f"{self.pjroot}/src/", '')
            # 該当ファイルが除外設定の場合はcontinue
            if self._is_ignore_file(file_rel_path):
                continue

            # ルートフォルダからのパスを作成
            topath = self.get_pj_dist_root(environment) + '/{file_rel_path}'

            # ファイルを置き換える設定の場合、置き換え後のファイルを作成
            if self._is_replace_file_content(file_rel_path):
                # 置き換え後の文字列を取得
                content = self._get_target_content(file)
                # 置き換え実施
                content = self._get_replaced_text(content)
                # contentの内容を、topath.replace('.temp', '')のファイルに書き込む
                self._write_replaced_content(topath.replace('.temp', ''), content)
            # それ以外は、ファイルをそのままコピー
            else:
                self._copy_file(file, topath)

    def _get_target_content(self, path: str):
        """ 指定のファイルの内容を取得 """
        with open(path, 'r') as path:
            content = path.read()
        return content

    def _get_replaced_text(self, content: str) -> str:
        """ 置き換え後のテキストを取得 """
        for key, value in self.config.replacements.items():
            content = content.replace(f'{{{{{key}}}}}', value)

        return content

    def _get_all_files(self, directory):
        """指定のフォルダ以下の全ファイル一覧を取得"""
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def _is_ignore_file(self, file_name: str) -> bool:
        """ 除外するファイルかどうか """
        # self.setting.ignore_filesでループし、ignore_fileが、ファイル名にワイルドカード形式で合致した場合、Trueを返す
        for ignore_file in self.config.ignore_files:
            if fnmatch.fnmatch(file_name, ignore_file):
                return True
        return False

    def _is_replace_file_content(self, file_rel_path: str) -> bool:
        """ ファイルの中身を置き換える設定かどうか """
        # is_only_replace_tempの設定がtrueなら置き換える
        if not self.config.is_only_replace_temp:
            return True
        # 指定したfileの末尾が".temp"かどうかで判定
        return file_rel_path.endswith('.temp')

    def _copy_file(self, frompath: str, topath: str):
        """ ファイルのコピー """
        os.makedirs(os.path.dirname(topath), exist_ok=True)
        shutil.copy(frompath, topath)

    def _write_replaced_content(self, topath: str, content: str):
        """ 置き換え後のファイルを書き込む """
        os.makedirs(os.path.dirname(topath), exist_ok=True)
        with open(topath, 'w') as output_file:
            output_file.write(content)
