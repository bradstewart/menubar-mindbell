"""
py2app build script for MindBell

Usage:
    python setup.py py2app
"""
from setuptools import setup

APP = ['mindbell.py']
DATA_FILES = [
    ('media', ['media/icon.png', 'media/jap-rin-1.aiff'])
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'media/icon.png',
    'plist': {
        'CFBundleName': 'MindBell',
        'CFBundleDisplayName': 'MindBell',
        'CFBundleGetInfoString': "Meditation Bell Timer",
        'CFBundleIdentifier': "art.bstew.mindbell",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Personal Use",
        'LSUIElement': True,  # Hide from dock (menu bar only app)
    },
    'packages': ['rumps', 'AppKit', 'Foundation', 'objc'],
    'includes': ['jaraco.text', 'packaging', 'pkg_resources'],
    'excludes': ['tkinter', 'matplotlib'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)