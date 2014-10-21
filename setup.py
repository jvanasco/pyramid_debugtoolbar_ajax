"""pyramid_debugtoolbar_ajax installation script.
"""
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
README = README.split("\n\n", 1)[0] + "\n"

requires = ['pyramid_debugtoolbar>=2.2', ]

setup(
    name="pyramid_debugtoolbar_ajax",
    version="0.0.1",
    description="Ajax support for pyramid_debugtoolbar",
    long_description=README,
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="web pyramid",
    packages=['pyramid_debugtoolbar_ajax'],
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_debugtoolbar_ajax",
    license="MIT",
    zip_safe=False,
    install_requires=requires,
    test_suite="tests",
)
