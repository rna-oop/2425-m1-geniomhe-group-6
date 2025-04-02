import os
import subprocess
import sys
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Function to run a terminal command
def install_viennarna():
    
    
    result = subprocess.run("pip list | grep ViennaRNA", shell=True, capture_output=True, text=True)
    if "ViennaRNA" in result.stdout:
        print("ViennaRNA is already installed.")
        return

    try:
        if not os.path.exists("tools"):
            os.makedirs("tools")
        os.chdir("tools")

        subprocess.check_call(["curl", "-O", "https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_7_x/ViennaRNA-2.7.0.tar.gz"])

        subprocess.check_call(["tar", "-zxvf", "ViennaRNA-2.7.0.tar.gz"])

        # Change to the extracted directory
        os.chdir("ViennaRNA-2.7.0")

        # Configure, make, and install ViennaRNA
        subprocess.check_call(["./configure"])
        subprocess.check_call(["make"])
        subprocess.check_call(["sudo", "make", "install"])

        print("ViennaRNA installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during ViennaRNA installation: {e}")
        sys.exit(1)

install_viennarna()

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