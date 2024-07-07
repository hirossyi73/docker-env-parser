from models.project import Project


class ProjectMock(Project):
    @property
    def pj_root(self):
        """Root path of the project"""
        if self.config.is_multi_project_mode:
            return f"samples/{self.name}"
        return self.name
