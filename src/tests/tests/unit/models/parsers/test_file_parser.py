import unittest
from models.parser.file_parser import FileParser
from tests.models.config_mock import ConfigMock


class TestFileParser(unittest.TestCase):
    def setUp(self):
        self.base_path = "src/tests/test_files/project_config/replacement_files"
        self.config = ConfigMock(None, "development")
        pass

    def test_parse_replace(self):
        parser = FileParser(self.config, "foo", f"{self.base_path}/foo.txt")
        parser.key = "foo"
        parser.file_path = f"{self.base_path}/foo.txt"
        parser.folder_path = f"{self.base_path}"
        self.assertEqual(parser.parse("This is {{foo}}").strip(), "This is bar")

    def test_parse_not_replace(self):
        parser = FileParser(self.config, "foo", f"{self.base_path}/foo.txt")
        parser.file_path = f"{self.base_path}/foo.txt"
        parser.folder_path = f"{self.base_path}"
        self.assertEqual(parser.parse("This is {{aaa}}").strip(), "This is {{aaa}}")

    def test_parse_break(self):
        parser = FileParser(self.config, "break", f"{self.base_path}/break.txt")
        parser.file_path = f"{self.base_path}/break.txt"
        parser.folder_path = f"{self.base_path}"
        self.assertEqual(parser.parse("This is break test.\n{{break}}").strip(
        ), "This is break test.\nThis\nis\nmy\nname.")
