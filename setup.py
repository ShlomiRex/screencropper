from setuptools import setup, find_packages

setup(
    name='screencropper',
    version='0.1.2',
    description='A Python library for selecting regions of the screen and taking screenshot, and outputting the coordinates and image of the selected region.',
    author='Shlomi Domnenko',
    author_email='vgtvgy1@gmail.com',
    url='https://github.com/ShlomiRex/screencropper',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    keywords=["python", "screen", "capture", "region", "crop"],
    license="Unlicense",
    install_requires=["Pillow", "opencv-python", "pyautogui", "tk"],
    entry_points={
        "console_scripts": [
            "screencropper = screencropper:run",
        ]
    },
    long_description=
        """A Python library for selecting regions of the screen and taking screenshot,
        and outputting the coordinates and image of the selected region.
        
        Github repository: https://github.com/ShlomiRex/screencropper
        """
)
