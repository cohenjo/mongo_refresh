from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call


def install_autocomplet():
    call(['mongo_refresh','install-autocomplet'])

class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        install_autocomplet()


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        install_autocomplet()


setup(
    name='mongo_refresh',
    version='0.1',
    py_modules=['mongo_refresh'],
    include_package_data=True,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    install_requires=[
        'ruamel.yaml',
        'tendo',
        'requests',
        'colorama==0.3.9',
        'wheel==0.24.0',
        'Click',
        'click_completion',
        'yaspin',
        'PyInquirer',
        'deepmerge',
        'Pygments',
        'tabulate',
        'pydash',
        'pymongo',
        'geocoder',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        mongo_refresh=mongo_refresh:cli
    ''',
)
