from os.path import abspath, join
from pathlib import Path


class DesktopModel:
    def __init__(self, app_name, desktop_configs_dir):
        self.filepath = desktop_configs_dir
        self.header = 'Desktop Entry'
        self.type = 'Application'
        self.name = app_name
        self.comment = ''
        self.icon = ''
        self.exec = ''
        self.terminal = False
        self.categories = []

        self.categories.append(app_name)

    def input_comment(self):
        self.comment = str(input('App description: '))

    def input_categories(self):
        while True:
            category = str(input('App category: '))
            if category == '':
                break
            self.categories.append(category)

    def input_is_terminal(self):
        term = str(input('Is terminal app? (y/N) '))
        if term == 'y' or term == 'Y':
            self.terminal = True

    def get_icon_path(self):
        return self.icon

    def set_icon_path(self, icon_path):
        self.icon = icon_path

    def get_exec_path(self):
        return self.exec

    def set_exec_path(self, exec_path):
        self.exec = exec_path

    def get_filename(self):
        return join(self.filepath, f'{self.name}.desktop')

    def generate_file(self):
        with open(self.get_filename(), 'w+') as desktop:
            desktop.write(f'[{self.header}]\n')
            desktop.write(f'Type={self.type}\n')
            desktop.write(f'Name={self.name}\n')
            desktop.write(f'Comment={self.comment}\n')
            if self.icon != '':
                desktop.write(f'Icon={self.icon}\n')
            desktop.write(f'Exec={self.exec}\n')
            desktop.write(f'Terminal={"True" if self.terminal else "False"}\n')
            desktop.write(f'Categories={";".join(self.categories)}\n')
