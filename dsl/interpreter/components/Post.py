from .Component import *
from .Values import *

COMPONENT = "Post"

class Post(Component):
    DEFAULT_ARGS = {
        "title": "Example Post",
        "content": "This is content",
        "icon": "",
        "image": "{process.env.PUBLIC_URL + '/logo.png'}",
        "size": "medium",
    }
    ARG_TO_ATTR_MAP = {
        "size": {
            "small": 240,
            "medium": 480,
            "large": 720
        }
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS,
                         args, rows, self.ARG_TO_ATTR_MAP)
        if len(rows) != 0:
            raise EvaluationError(COMPONENT, "post is not expecting any rows in it")

    def getSize(self):
        return self.ARG_TO_ATTR_MAP["size"][self.args["size"]]
    
    def getCover(self):
        cover = ""
        if self.getParamVal("image") != "":
            img = Image({"src": self.getParamVal("image"), "width": str(self.getSize()), "height": str(self.getSize())}, [])
            cover = f"cover={{{img.render()}}}"
        return cover

    def getIcon(self):
        avatar = ""
        if self.getParamVal("icon") != "":
            avatar = f'avatar="{self.getParamVal("icon")}"'
        return avatar

    def render(self):
        return f"""
            <Card
                hoverable
                style={{{{ width: {self.getSize()} }}}}
                {self.getCover()}
            >
                <Meta
                    title="{self.getParamVal("title")}"
                    description="{self.getParamVal("content")}"
                    {self.getIcon()}
                />
            </Card>
        """