"""Installs the Dominion simulator."""
from setuptools import setup


setup(
    name='Dominion',
    version='0.0',
    py_modules=['play_game'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dominion=play_game:play_game
    ''',
)
