
import os
import yaml


class Helper:
    @staticmethod
    def get_yaml_config(path: str) -> dict:
        """ yamlファイルから値をマージする """
        if not os.path.isfile(path):
            return {}
        with open(path, encoding='utf-8')as f:
            r = yaml.safe_load(f)
            # 値が存在してれば、マージ
            if r is None:
                return {}
            return r
