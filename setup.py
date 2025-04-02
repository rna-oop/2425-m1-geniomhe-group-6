import os
import subprocess
import sys
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="rnalib",  
    version="0.0.0",
    author="Joelle ASSY, Rayane ADAM",  
    description="object-oriented programming project with RNA structures manipulation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rna-oop/2425-m1-geniomhe-group-6", 
    packages=find_packages(),
    install_requires=requirements,  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Uses match-case, requires Python 3.10+
)