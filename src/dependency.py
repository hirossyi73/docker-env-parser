from factories.project_factory import ProjectFactory, ProjectFactoryBase
from injector import Injector
from models.config import GlobalConfig
from models.config import GlobalConfig
from injector import Injector, singleton


class Dependency():
    """Class that resolves dependencies for the main process"""

    def __init__(self) -> None:
        # Load the function that sets up the dependencies
        self.injector = Injector(self.__class__.config)

    # Method to set up the dependencies
    @classmethod
    def config(cls, binder):
        # Load the common configuration file
        global_config = GlobalConfig()
        global_config.init_config(None, None)
        binder.bind(GlobalConfig, to=global_config, scope=singleton)

        # bind the ProjectFactoryBase class to the ProjectFactory class
        project_factory = ProjectFactory()
        binder.bind(ProjectFactoryBase, to=project_factory, scope=singleton)

    # When passing arguments to injector.get(), it resolves the dependencies and creates an instance
    def resolve(self, cls):
        return self.injector.get(cls)
