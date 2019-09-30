from .Component import *


class Nav(Component):

    def render(self):
        return f"""
            <Sider style={{{{ height: '100vh', left: 0, background: 'azure'}}}}>
                <Menu
                    theme="light"
                    mode="inline">
                    <Menu.Item key="1">nav 1</Menu.Item>
                    <Menu.Item key="2">nav 2</Menu.Item>
                    <Menu.Item key="3">nav 3</Menu.Item>
                </Menu>
            </Sider>"""
