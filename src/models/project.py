import fnmatch
import os
import shutil
from models.config import Config
from models.const import FolderName


class Project:
    name: str
    environment: str
    config: Config

    def __init__(self, name: str, environment: str, config: Config):
        self.name = name
        self.environment = environment
        self.config = config

    @property
    def pj_root(self):
        """path of the project"""
        if self.config.is_multi_project_mode:
            return f"{FolderName.TARGET_ROOT_FOLDER.value}/{self.name}"
        return self.name

    @property
    def root_path(self):
        """Root path of the project"""
        return f"{self.pj_root}/{FolderName.REPLACE_TARGET.value}"

    def build(self):
        # Skip if it's an ignored configuration
        if self.config.is_ignore:
            return

        # Get a list of files in the "temp" folder
        files = self._get_files()
        for file in files:
            # Get the file name without the path up to "src/"
            file_rel_path = file.replace(f"{self.root_path}/", '')
            # Skip if the file is in the ignore list
            if self._is_ignore_file(file_rel_path):
                continue

            # Create the path relative to the root folder
            to_path = self._get_pj_dist_root() + f'/{file_rel_path}'

            # If it's a file to be replaced, create the replaced file
            if self._is_replace_file_content(file_rel_path):
                # Get the content to be replaced
                content = self._get_target_content(file)
                # Perform the replacement
                content = self._get_replaced_text(content)
                # Write the content to the file specified by to_path.replace('.temp', '')
                self._write_replaced_content(to_path.replace('.temp', ''), content)
            # Otherwise, copy the file as is
            else:
                self._copy_file(file, to_path)

    def _get_pj_dist_root(self):
        """Get the root path of the project's dist"""
        root_path = f'{FolderName.OUTPUT_ROOT.value}/docker-{self.environment}/{self.name}'
        if self.config.is_multi_project_mode:
            return f'{root_path}/{self.name}'
        return root_path

    def _get_target_content(self, path: str):
        """Get the content of the specified file"""
        with open(path, 'r') as path:
            content = path.read()
        return content

    def _get_replaced_text(self, content: str) -> str:
        """Get the replaced text"""
        for _, parser in self.config.get_parsers().items():
            # Use the parser's parse method to replace the content
            content = parser.parse(content)

        return content

    def _get_files(self) -> dict[str, str]:
        """
        Get a list of all files in the specified directory. Consider the environment.
        key: the real file path. 
        value: removed environment file path
        """
        tmp_result = self._get_dir_file_paths()

        # Re-loop result array. And if contains "." at least 2, check env in arg[-2].
        # And if match arg[-2], set as key: arg[-2] value: arg[-1]
        result = {}
        for file_path in tmp_result:
            dir_name = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_keys = file_name.split('.')
            # if file_keys length is less than 3(ex. "sample.txt"), append it to result
            if len(file_keys) < 3:
                result[file_path] = file_path
                continue

            # If file_keys length is 3 or more(ex. "sample.development.txt"), check if the last-1 element is the environment
            if file_keys[-2] != self.environment:
                continue
            else:
                result[file_path] = dir_name + '/' + '.'.join(f"{file_keys[:-3]}.{file_keys[-1]}")

        return result

    def _get_dir_file_paths(self) -> list[str]:
        """Get a list of all files in the specified directory"""
        result = []
        for root, _, files in os.walk(self.root_path):
            for file in files:
                result.append(os.path.join(root, file))
        return result

    def _is_ignore_file(self, file_name: str) -> bool:
        """Check if it's an ignored file"""
        # Loop through self.setting.ignore_files and return True if ignore_file matches the file name using wildcard pattern
        for ignore_file in self.config.ignore_files:
            if fnmatch.fnmatch(file_name, ignore_file):
                return True
        return False

    def _is_replace_file_content(self, file_rel_path: str) -> bool:
        """Check if it's a file to replace its content"""
        # Return True if is_only_replace_temp setting is true
        if not self.config.is_only_replace_temp:
            return True
        # Check if the specified file ends with ".temp"
        return file_rel_path.endswith('.temp')

    def _copy_file(self, from_path: str, to_path: str):
        """Copy the file"""
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
        shutil.copy(from_path, to_path)

    def _write_replaced_content(self, to_path: str, content: str):
        """Write the replaced file content"""
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
        with open(to_path, 'w') as output_file:
            output_file.write(content)
