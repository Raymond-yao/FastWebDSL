from Component import *

class Header(Component):

    def __init__(self):
        super().__init__()

    def render(self):
        return f"""
            <Header>
                <Menu
                    theme="light"
                    mode="horizontal"
                    style={{{{ lineHeight: '64px' }}}}>
                    <Menu.Item key="1">nav 1</Menu.Item>
                    <Menu.Item key="2">nav 2</Menu.Item>
                    <Menu.Item key="3">nav 3</Menu.Item>
                </Menu>
            </Header>
        """
