"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
from plistlib import Plist
plist = Plist.fromFile('Info.plist')
plist.update(dict(
LSPrefersPPC=True,
))

APP = ['ProjectRei.py']
DATA_FILES = [('images', ['images/Easy_A_logo.png','images/Easy_A_logo_mini.png']),('save',['save/'])]
OPTIONS = {'iconfile':'./images/Easy_A.icns','packages': ['certifi',]}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
