#!/usr/bin/env python
from setuptools import setup
from game.const import APP_NAME, VERSION, PROJECT_DESC, PROJECT_URL

def readme():
    try:
        return open('README.md').read()
    except:
        return ""

setup(name=APP_NAME,
      version=VERSION,
      description=PROJECT_DESC,
      long_description=readme(),
      author='Martin Balmaceda',
      author_email='martin.balmaceda@gmail.com',
      url=PROJECT_URL,
      license='GNU GENERAL PUBLIC LICENSE',
      install_requires=['pyglet>=1.3.2'],
      include_package_data=True,
      zip_safe=False,
      scripts=['run_game.py'],
      packages=['game', 'plib', 'pyglet', 'data'],
      classifiers = [
        'Programming Language :: Python 3',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Intended Audience :: End Users/Desktop',
        ],
      )

