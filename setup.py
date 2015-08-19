import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), "reference_counter", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIERS = [
    'logbook'
    ]

setup(name="reference_counter",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          ],
      description="Signaling and hooking library",
      license="BSD3",
      author="Ayala Shachar",
      author_email="shachar.ayala@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/ayalash/reference_counter",

      install_requires=_INSTALL_REQUIERS,
      scripts=[],
      namespace_packages=[]
      )
