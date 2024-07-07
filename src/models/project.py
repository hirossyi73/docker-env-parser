import fnmatch
import os
import shutil
from models.config import Config


class Project:
    config: Config

    def __init__(self, name: str, config: Config):
        self.name = name
        self.config = config

    @property
    def pjroot(self):
        """Root path of the project"""
        if self.config.is_multi_project_mode:
            return f"templates/{self.name}"
        return "templates"

    def get_pj_dist_root(self, environment: str):
        """Get the root path of the project's dist"""
        if self.config.is_multi_project_mode:
            return f'dist/docker-{environment}/{self.name}'
        return f'dist/docker-{environment}'

    def build(self, environment: str):
        # Skip if it's an ignored configuration
        if self.config.is_ignore:
            return

        # Get a list of files in the "temp" folder
        files = self._get_all_files(f"{self.pjroot}/src")
        for file in files:
            # Get the file name without the path up to "src/"
            file_rel_path = file.replace(f"{self.pjroot}/src/", '')
            # Skip if the file is in the ignore list
            if self._is_ignore_file(file_rel_path):
                continue

            # Create the path relative to the root folder
            topath = self.get_pj_dist_root(environment) + f'/{file_rel_path}'

            # If it's a file to be replaced, create the replaced file
            if self._is_replace_file_content(file_rel_path):
                # Get the content to be replaced
                content = self._get_target_content(file)
                # Perform the replacement
                content = self._get_replaced_text(content)
                # Write the content to the file specified by topath.replace('.temp', '')
                self._write_replaced_content(topath.replace('.temp', ''), content)
            # Otherwise, copy the file as is
            else:
                self._copy_file(file, topath)

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

    def _get_all_files(self, directory):
        """Get a list of all files in the specified directory"""
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

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

    def _copy_file(self, frompath: str, topath: str):
        """Copy the file"""
        os.makedirs(os.path.dirname(topath), exist_ok=True)
        shutil.copy(frompath, topath)

    def _write_replaced_content(self, topath: str, content: str):
        """Write the replaced file content"""
        os.makedirs(os.path.dirname(topath), exist_ok=True)
        with open(topath, 'w') as output_file:
            output_file.write(content)
