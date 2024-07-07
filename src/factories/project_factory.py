from abc import ABC, abstractmethod
from models.config import Config
from models.const import FolderName
from models.project import Project


class ProjectFactoryBase(ABC):
    """Abstract Factory for creating Project instances"""
    @abstractmethod
    def make(self, name: str, environment: str, config: Config) -> Project:
        pass


class ProjectFactory(ProjectFactoryBase):
    """Factory for creating Project instances(default)"""

    def make(self, name: str, environment: str, config: Config) -> Project:
        local_config = Config(f'{FolderName.TARGET_ROOT_FOLDER.value}/{name}', environment)
        local_config.init_config(config)
        # Create a project class
        project = Project(name, environment, local_config)

        return project
