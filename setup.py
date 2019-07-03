from setuptools import setup
setup(
    name = 'unbabel_cli',
    version = '0.1.0',
    packages = ['unbabel_cli'],
    entry_points = {
        'console_scripts': [
            'unbabel_cli = unbabel_cli.__main__:main'
        ]
    })
