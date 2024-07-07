import unittest
from tests.models.project_mock import ProjectMock


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = ProjectMock()
        self.base_path = "src/tests/test_files/project_config"

    def test_get_dir_file_paths(self):
        self.project.get_dir_file_paths_callback = lambda base_path: [
            f'foo.txt',
            f'bar.txt',
            f'bar.develop.txt',
            f'baz.txt',
            f'baz.production.txt',
            f'qux.production.txt',
        ]

        self.project._get_dir_file_paths(self.base_path)
