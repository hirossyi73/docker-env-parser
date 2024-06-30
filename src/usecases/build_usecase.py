

import os
from models.config import Config, GlobalConfig
from models.project import Project


class BuildUsecase:
    """ build files usecase """
    global_config: GlobalConfig

    def __init__(self, config: Config):
        self.global_config = config

    def build(self):
        """ build files """

        for env in self.global_config.environments:
            for project in self._get_projects(env):
                project.build(env)

    def _get_projects(self, environment: str) -> list[Project]:
        """ ファイルパスを使用して、プロジェクト一覧を取得 """

        # マルチプロジェクトモードでない場合、templatesフォルダ直下のみを対象とする
        if not self.global_config.is_multi_project_mode:
            # templatesフォルダ直下のフォルダ一覧を取得
            local_config = Config()
            local_config.init_config("templates", environment, self.global_config)
            return [Project("templates", local_config)]

        # マルチプロジェクトモードな場合、templatesフォルダ直下のフォルダ一覧を取得
        dirs = os.listdir('templates')
        projects = []
        for name in dirs:
            local_config = Config()
            local_config.init_config(f'templates/{name}', environment, self.global_config)
            # プロジェクトクラスを作成
            project = Project(name, local_config)
            # プロジェクトクラスをリストに追加
            projects.append(project)

        return projects
