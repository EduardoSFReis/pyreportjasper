import io
import os
import re
from setuptools import setup, find_packages
from collections import OrderedDict
import subprocess

def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        init_py = f.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

with io.open("README.md", "rt", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyreportjasperbytesUVV",
    version=get_version("pyreportjasper"),
    url="https://github.com/EduardoSFReis/pyreportjasper",
    download_url="https://pypi.org/project/pyreportjasperbytesUVV/" + get_version("pyreportjasper"),
    project_urls=OrderedDict((
        ("Documentation", "https://pyreportjasper.readthedocs.io/en/master/"),
        ("Code", "https://github.com/EduardoSFReis/pyreportjasper"),
        ("Issue tracker", "https://github.com/EduardoSFReis/pyreportjasper/issues"),
    )),
    license="GPLv3",
    author="Eduardo Soares Franco Reis",
    author_email="edufrancoreis@hotmail.com",
    maintainer="Eduardo Soares Franco Reis",
    maintainer_email="edufrancoreis@hotmail.com",
    keywords="report jasper python",
    description="This package aims to be a solution to compile and process JasperReports (.jrxml & .jasper files).",
    long_description=long_description,
    long_description_content_type="text/markdown",  # <- IMPORTANTE
    packages=find_packages(),
    install_requires=["jpype1"],
    extras_require={
        "docs": [
            "readthedocs-sphinx-ext",
            "sphinx",
            "sphinx-rtd-theme",
            "recommonmark",
            "commonmark",
            "mock",
            "docutils",
            "Pygments",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
