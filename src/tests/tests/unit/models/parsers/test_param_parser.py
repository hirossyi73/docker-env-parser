import unittest
from models.parser.param_parser import ParamParser
from tests.models.config_mock import ConfigMock


class TestParamParser(unittest.TestCase):
    def setUp(self):
        self.config = ConfigMock(None, "development")

    def test_parse_replace(self):
        parser = ParamParser(self.config, "foo", "bar")
        self.assertEqual(parser.key, "foo")
        self.assertEqual(parser.value, "bar")
        self.assertEqual(parser.parse("This is {{foo}}"), "This is bar")

    def test_parse_not_replace(self):
        parser = ParamParser(self.config, "foo", "bar")
        self.assertEqual(parser.key, "foo")
        self.assertEqual(parser.value, "bar")
        self.assertEqual(parser.parse("This is {{aaa}}"), "This is {{aaa}}")
