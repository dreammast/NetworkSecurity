from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """this function will return the list of requirements"""
    requirement_list = []
    try:
        with open('requirements.txt') as file:
            # read lines from the file 
            lines = file.readlines()
            for line in lines:
                requirements = line.strip()
                # ignore empty llines -e .
                if requirements and requirements!="-e .":
                    requirement_list.append(requirements)
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
    return requirement_list

setup(
    name = "Network_security",
    version = "0.0.1",
    author = "Nale Dushyanth",
    author_email = "naledushyanth@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)