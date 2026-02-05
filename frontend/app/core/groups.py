
from app.client.apps import (
    APIException,
    get_groups
)

class Group:
    def __init__(self, application):
        self.group_index = {}
        self.groupings = {}
        self.group_by = None
        
        try:
            self.groups = get_groups(application)
            for index, g in enumerate(self.groups["groupnames"]):
                self.group_index[g] = index
            for g in self.groups['groupings']:
                comp = g['name']
                groups = g['groups']
                self.groupings[comp] = groups
            self.group_by = self.groups["groupnames"][0]

        except APIException:
            self.groups = None


