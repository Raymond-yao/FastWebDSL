from .Component import *
from .Content import *
from .Footer import *
from .Header import *
from .Link import *
from .Nav import *
from .Page import *
from .Post import *
from .Row import *
from .Values import *

class ComponentFactory:

    def __init__(self):
        self.COMPONENTS = {}
        self.COMPONENT_WITH_ROW = []
        self.COMPONENT_WITH_PARAMS = []

    def get(self, component_name):
        return self.COMPONENTS[component_name]

ALL_COMPONENTS = {
    "Header": Header,
    "Nav": Nav,
    "Footer": Footer,
    "Content": Content,
    "Link": Link,
    "Row": Row,
    "Text": Text,
    "Image": Image,
    "Page": Page,
    "Post": Post,
    "Video": None, # TODO
    "Button": Link
}

class RealComponentFactory(ComponentFactory):

    def __init__(self):
        super().__init__()
        self.COMPONENTS = ALL_COMPONENTS