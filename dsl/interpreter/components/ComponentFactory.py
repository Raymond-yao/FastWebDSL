from .Component import *
from .Content import *
from .Header import *
from .Nav import *
from .Page import *
from .Row import *
from .Values import *

class ComponentFactory:

    def __init__(self):
        self.COMPONENTS = {}
        self.COMPONENT_WITH_ROW = []
        self.COMPONENT_WITH_PARAMS = []

    def get(self, component_name):
        return self.COMPONENTS[component_name]

    def has_row(self, component_name):
        return component_name in self.COMPONENT_WITH_ROW
    
    def has_attribute(self, component_name):
        return component_name in self.COMPONENT_WITH_PARAMS

class RealComponentFactory(ComponentFactory):

    def __init__(self):
        super().__init__()
        self. COMPONENTS = {
            "Page": Page,
            "Nav": Nav,
            "Header": Header,
            "Content": Content,
            "Text": Text
        }
        self.COMPONENT_WITH_ROW = ["Page", "Nav", "Header", "Content"]
        self.COMPONENT_WITH_PARAMS = ["Nav", "Header", "Content"]