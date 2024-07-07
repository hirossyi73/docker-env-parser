import unittest
from models.parser.param_parser import ParamParser
from tests.models.config_mock import ConfigMock, GlobalConfigMock


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = ConfigMock()
        self.base_path = "src/tests/test_files/project_config"

    def test_default_props(self):
        self.assertEqual(self.config.replacements, {})
        self.assertEqual(self.config.is_ignore, False)
        self.assertEqual(self.config.is_auto_merge_config, True)
        self.assertEqual(self.config.is_only_replace_temp, False)
        self.assertEqual(self.config.is_multi_project_mode, False)
        self.assertEqual(self.config.replacement_files, {})
        self.assertEqual(self.config.ignore_files, [])
        self.assertEqual(self.config.get_parsers(), {})

    def test_merge_config_dict_1(self):
        base_config = {'key1': 'value1', 'key2': 'value2'}
        config = {'key2': 'new_value2', 'key3': 'value3'}

        merged_config = self.config._merge_config_dict(config, base_config)
        self.assertIsInstance(merged_config, dict)
        self.assertEqual(merged_config, {"key1": "value1", "key2": "new_value2", 'key3': 'value3'})

    def test_merge_config_dict_2(self):
        base_config = None
        config = {'key2': 'new_value2', 'key3': 'value3'}

        merged_config = self.config._merge_config_dict(config, base_config)
        self.assertIsInstance(merged_config, dict)
        self.assertEqual(merged_config, {'key2': 'new_value2', 'key3': 'value3'})

    def test_merge_config_dict_2(self):
        base_config = {'key1': 'value1', 'key2': 'value2'}
        config = None

        merged_config = self.config._merge_config_dict(config, base_config)
        self.assertIsInstance(merged_config, dict)
        self.assertEqual(merged_config, {'key1': 'value1', 'key2': 'value2'})

    def test_get_config_dict_from_path(self):
        path = f"{self.base_path}/config.yml"
        config_dict = self.config._get_config_dict_from_path(path)
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict, {
            "replacements": {
                "foo": "bar",
                "baz": "qux",
            },
            "settings": {
                "is_ignore": True,
                "is_auto_merge_config": False,
                "is_multi_project_mode": True,
            }
        })

    def test_read_string_from_path(self):
        path = f"{self.base_path}/test.txt"
        result = self.config._read_string_from_path(path)
        self.assertIsInstance(result, str)
        self.assertEqual(result.strip(), "This is test for reading text.")

    def test_get_config_value(self):
        config = {"key": "value"}
        keys = ["key"]
        value = self.config._get_config_value(config, keys)
        self.assertEqual(value, "value")

    def test_get_config_value_array(self):
        config = {"replacements": ["value1", "value2", "value3"]}
        keys = ["replacements"]
        value = self.config._get_config_value(config, keys)
        self.assertEqual(value, ["value1", "value2", "value3"])

    def test_get_config_value_deep_dict(self):
        config = {"settings": {'is_ignore': True, 'is_auto_merge_config': False,
                               'is_multi_project_mode': True, 'is_only_replace_temp': True}}
        keys = ["settings", "is_ignore"]
        value = self.config._get_config_value(config, keys)
        self.assertEqual(value, True)

    def test_get_config_dict_from_yaml(self):
        yaml_string = "key: value"
        config_dict = self.config._get_config_dict_from_yaml(yaml_string)
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict, {"key": "value"})

    def test_get_replacement_files(self):
        base_path = "/path/to/base"
        replacement_files = self.config._get_replacement_files(base_path)
        self.assertIsInstance(replacement_files, dict)
        self.assertEqual(replacement_files, {})

    def test_init_config(self):
        self.config.init_config(self.base_path, "development")

        self.assertEqual(self.config.replacements, {'foo': 'bar', 'baz': 'qux'})
        self.assertEqual(self.config.is_ignore, True)
        self.assertEqual(self.config.is_auto_merge_config, False)
        self.assertEqual(self.config.is_only_replace_temp, False)
        self.assertEqual(self.config.is_multi_project_mode, True)
        self.assertEqual(len(self.config.replacement_files), 2)
        self.assertEqual(self.config.ignore_files, [])

        # test get_parsers
        parsers = self.config.get_parsers()
        parser : ParamParser = parsers.get("foo")
        self.assertTrue(parser is not None)
        self.assertEqual(parser.parse("This is {{foo}}"), "This is bar")

        parser : ParamParser = parsers.get("baz")
        self.assertTrue(parser is not None)
        self.assertEqual(parser.parse("This is {{baz}}"), "This is qux")

    def test_init_config_use_global_config(self):
        global_config = GlobalConfigMock()
        global_config.set_is_multi_project_mode(False)
        global_config.set_is_only_replace_temp(True)
        self.config.init_config(self.base_path, "development", global_config)

        self.assertEqual(self.config.replacements, {'foo': 'bar', 'baz': 'qux'})
        self.assertEqual(self.config.is_ignore, True)
        self.assertEqual(self.config.is_auto_merge_config, False)
        self.assertEqual(self.config.is_only_replace_temp, True)
        self.assertEqual(self.config.is_multi_project_mode, True)
        self.assertEqual(len(self.config.replacement_files), 2)
        self.assertEqual(self.config.ignore_files, [])

        # test get_parsers
        parsers = self.config.get_parsers()
        parser : ParamParser = parsers.get("foo")
        self.assertTrue(parser is not None)
        self.assertEqual(parser.parse("This is {{foo}}"), "This is bar")

        parser : ParamParser = parsers.get("baz")
        self.assertTrue(parser is not None)
        self.assertEqual(parser.parse("This is {{baz}}"), "This is qux")
