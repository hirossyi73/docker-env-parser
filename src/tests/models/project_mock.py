from typing import Callable, Optional
from models.project import Project


class ProjectMock(Project):
    get_dir_file_paths_callback: Optional[Callable] = None

    def _get_dir_file_paths(self, directory: str) -> list[str]:
        if self.get_dir_file_paths_callback is not None:
            return self.get_dir_file_paths_callback(directory)
        return super()._get_dir_file_paths(directory)
