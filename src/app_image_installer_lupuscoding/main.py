import click
from pathlib import Path
from os import W_OK, access, mkdir
from os.path import isdir, join, abspath, isfile
from shutil import move
from termcolor import colored
from .desktop_file_model import DesktopModel


@click.command()
@click.argument('app_name')
@click.argument('filepath')
@click.option('-i', '--icon', default='', prompt='Icon path (png/svg)', type=str, help='Path to app icon')
def install(app_name, filepath, icon):
    """Install an AppImage

    The AppImage file at FILEPATH will be installed. The name will be changed to APP_NAME for convenience.
    """
    app_dir = f'{Path.home()}/Applications'
    desktop_configs_dir = abspath(join(Path.home(), '.local/share/applications'))

    if check_dir(app_dir, 'Applications folder') is False:
        choice_create = str(input('Folder does not exist. Create? (y/N) '))
        if choice_create != 'y' and choice_create != 'Y':
            print_err('Applications folder does not exist and could not be created')
        print(f'Trying to create Applications folder...')
        mkdir(app_dir, 0o664)
        if check_dir(app_dir, 'Applications folder') is False:
            print_err('Unable to create and access folder')

    if not check_dir(desktop_configs_dir, 'Configuration folder'):
        print_err(f'Configuration folder {desktop_configs_dir} is not writable')

    if not isfile(filepath):
        print_err(f'AppImage {filepath} could not be found')
    print(f'AppImage: {colored("OK", "green")}')

    if not isfile(icon) and icon != '':
        print_err(f'Icon at {icon} could not be found')
    print(f'Icon file: {colored("OK", "green")}')

    # init model
    print(colored('Please fill the following fields', 'light_blue'))
    model = DesktopModel(app_name, desktop_configs_dir)
    model.input_comment()
    model.input_categories()
    model.input_is_terminal()

    print('Installing', end='')
    print('.', end='')
    # Moving {app_name} from {filepath} to {app_dir}
    model.set_exec_path(abspath(join(app_dir, f'{app_name}.AppImage')))
    move(filepath, model.get_exec_path())
    print('.', end='')
    if icon != '':
        # Moving icon from {icon} to {app_dir}
        model.set_icon_path(abspath(join(app_dir, f'{app_name}.png')))
        move(icon, model.get_icon_path())
    print('.', end='')
    # Creating desktop configuration file...
    model.generate_file()
    print('.')
    print(colored(f'{app_name} was installed successful.', 'green'))

def check_dir(app_dir, message):
    """Check if directory exists and is writable"""
    print(f'{message}:', end=' ')
    if isdir(app_dir) and access(app_dir, W_OK):
        print(colored('OK', 'green'))
        return True
    print(colored('NOK', 'red'))
    return False

def print_err(msg):
    print(colored(f'ERR: {msg}', 'red'))
    exit(1)
