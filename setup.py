from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='screencropper',
    version='0.1.0',
    description='A Python library for selecting regions of the screen and outputting the coordinates or screenshot of the selected region.',
    author='Shlomi Domnenko',
    author_email='vgtvgy1@gmail.com',
    url='https://github.com/ShlomiRex/screencropper',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    keywords=["python", "screen", "capture", "region", "crop"],
    license="Unlicense",
    install_requires=required,
)
