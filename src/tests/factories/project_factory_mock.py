from factories.project_factory import ProjectFactoryBase
from models.config import Config
from models.project import Project
from tests.models.project_mock import ProjectMock


class ProjectFactoryMock(ProjectFactoryBase):
    """Factory for creating Project instances(default)"""

    def make(self, name: str, environment: str, config: Config) -> Project:
        # Create a project class
        return ProjectMock(name, environment, config)
