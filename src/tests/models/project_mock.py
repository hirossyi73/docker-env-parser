from models.project import Project


class ProjectMock(Project):
    @property
    def pjroot(self):
        """Root path of the project"""
        if self.config.is_multi_project_mode:
            return f"templates/{self.name}"
        return self.name
