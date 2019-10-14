from .Component import *
from .Values import *
from .Link import *


COMPONENT = "Header"


class Header(Component):
    DEFAULT_ARGS = {
        "title": "tab",
        "subtitle": "",
        "tag": "",
        "icon": "",
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)

    def render(self):
        headerFactory = HeaderFactory(self.args, self.rows)
        return f"""
        <PageHeader
          {headerFactory.getAvatar()}
          title="{self.getParamVal("title")}"
          subTitle="{self.getParamVal("subtitle")}"
          {headerFactory.getTags()}
          {headerFactory.getExtras()} 
        >
        </PageHeader>
        """


class HeaderFactory:
    def __init__(self, args, rows):
        self.args = args
        self.rows = rows

    def getAvatar(self):
        avatar = ""
        if self.args["icon"] != "":
            avatar = f'avatar={{{{ src: "{self.args["icon"]}" }}}}'
        return avatar

    def getTags(self):
        tag = ""
        if self.args["tag"] != "":
            tag = f'tags={{<Tag color="blue">{self.args["tag"]}</Tag>}}'
        return tag

    def getExtras(self):
        if len(self.rows) == 0:
            return ""
        if len(self.rows) != 1:
            raise EvaluationError(
                COMPONENT, "Header expects to only have one row of items")
        extras = "extra={["
        for i, item in enumerate(self.rows[0]):
            if isinstance(item, Text):
                items += f'<Button type="link" key="{i}">{item.getParamVal("text")}</Button>\n'
            elif isinstance(item, Link):
                items += item.render() + "\n"
            else:
                raise EvaluationError(
                    COMPONENT, "only Text and Link components are allowed")
        return extras + "]}"
