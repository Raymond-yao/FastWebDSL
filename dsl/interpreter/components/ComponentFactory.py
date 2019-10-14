from .Component import *
from .Content import *
from .Footer import *
from .Header import *
from .Link import *
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
        self.COMPONENTS = {
            "Header": Header,
            "Nav": Nav,
            "Footer": Footer,
            "Content": Content,
            "Link": Link,
            "Row": Row,
            "Text": Text,
        }
        self.COMPONENT_WITH_ROW = list(self.COMPONENTS.keys())
        self.COMPONENT_WITH_PARAMS = list(self.COMPONENTS.keys())