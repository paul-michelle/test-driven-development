import os
import dotenv
from django.core.management import utils
from fabric.contrib.files import exists, sed, append
from fabric.api import env, local, run

dotenv.load_dotenv()

REPO_LINK_VIA_SSH = os.getenv('REPO_LINK')
BRANCH = os.getenv('BRANCH')
DIR_WITH_SETTINGS_NAME = 'superlistsproject'
SECRET_KEY_LENGTH = 66

env.key_filename = os.getenv('KEY_PATH')


def deploy() -> None:
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = f'{site_folder}/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source_from_git(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_file(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder: str) -> None:
    site_sub_folders = ('database', 'static', 'virtualenv', 'source')
    for sub_folder in site_sub_folders:
        run(f'mkdir -p {site_folder}/{sub_folder}')


def _get_latest_source_from_git(source_folder: str) -> None:
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
        current_commit_on_pc = local('git log -n 1 --format=%H', capture=True)
        run(f'cd {source_folder} && git reset --hard {current_commit_on_pc}')
        return
    run(f'git clone {REPO_LINK_VIA_SSH} --branch {BRANCH} --single-branch {source_folder}')


def _update_settings(source_folder: str, site_name: str) -> None:
    settings_path = f'{source_folder}/{DIR_WITH_SETTINGS_NAME}/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}", "www.{site_name}"]')

    # secret_key_file = f'{source_folder}/{DIR_WITH_SETTINGS_NAME}/secret_key.py'
    # if not exists(secret_key_file):
        # chars = string.printable
        # key = ''.join(random.SystemRandom().choice(chars) for _ in range(SECRET_KEY_LENGTH))
    #     key = utils.get_random_secret_key()
    #     append(secret_key_file, f'SECRET_KEY = "{key}"')
    # append(settings_path, '\nfrom .secret_key_file import SECRET_KEY')


def _update_virtualenv(source_folder: str) -> None:
    virtualenv_folder = f'{source_folder}/../virtualenv'
    pip = f'{virtualenv_folder}/bin/pip'
    if not exists(pip):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{pip} install -r {source_folder}/requirements.txt')


def _update_static_file(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')
