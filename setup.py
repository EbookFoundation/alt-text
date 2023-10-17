"""
Sample setup.py file
"""
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="alt_text",
    version='{{VERSION_PLACEHOLDER}}',
    author="David Cruz",
    author_email="da.cruz@aol.com",
    description="A package used for finding, generating, and setting alt-text for images in HTML and EPUB files.",
    url = "https://github.com/EbookFoundation/alt_text",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["beautifulsoup4"],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)