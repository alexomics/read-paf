import re
from setuptools import setup

with open("readpaf.py", "r") as fh:
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fh.read(), re.MULTILINE)
    if match:
        __version__ = match.group(1)
    else:
        raise RuntimeError("Couldn't find __version__ string")

setup(
    name="readpaf",
    version=__version__,
    py_modules=["readpaf"],
    author="Alexander Payne",
    author_email="alexander.payne@nottingham.ac.uk",
    url="https://github.com/alexomics/read-paf",
    project_urls={
        "Bug Tracker": "https://github.com/alexomics/read-paf/issues",
        "Source Code": "https://github.com/alexomics/read-paf",
    },
    description="minimap2 PAF file reader",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    platforms="OS Independent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    extras_require={"pandas": "pandas"},
)
