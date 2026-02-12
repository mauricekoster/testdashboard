from nicegui import ui
from app.client import APIException

from app.client.projects import read_project
from app.models import ProjectPublic

class Project(object):
    def __init__(self, project_id: int):
        self.project_id = project_id
        self._project : ProjectPublic = read_project(project_id)
        print(self._project)
        

    def __getattribute__(self, name):
        if name.startswith('_project'):
            return object.__getattribute__(self, name)
        
        proj = object.__getattribute__(self, '_project')
        data = object.__getattribute__(proj, 'data')
        return getattr(data, name)