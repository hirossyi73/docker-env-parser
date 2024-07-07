import os
from factories.project_factory import ProjectFactoryBase
from models.config import GlobalConfig
from models.project import Project
from injector import inject


class BuildUsecase:
    """ build files usecase """
    global_config: GlobalConfig
    project_factory: ProjectFactoryBase

    @inject
    def __init__(self, config: GlobalConfig, project_factory: ProjectFactoryBase):
        self.global_config = config
        self.project_factory = project_factory

    def build(self):
        """ build files """

        for env in self.global_config.environments:
            for project in self._get_projects(env):
                project.build(env)

    def _get_projects(self, environment: str) -> list[Project]:
        """ Get a list of projects using file paths """
        project_names = self._get_project_names()
        projects = []
        for name in project_names:
            # Create a project class
            project = self.project_factory.make(name, environment, self.global_config)
            # Add the project class to the list
            projects.append(project)

        return projects

    def _get_project_names(self) -> list[str]:
        """ Get a list of project names """
        if not self.global_config.is_multi_project_mode:
            return ["templates"]

        dirs = os.listdir('templates')
        return dirs
