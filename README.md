# screencropper

A Python library that allows to select a region of screen and either take screenshot as an application or use the coordinates in their program as library.

## Usage

```python
from screencropper import crop

# Take screenshot of selected region
region, image = crop(take_screenshot=True)

print(region)
print(image)
```

## Build & install package locally

Build wheel: `python setup.py bdist_wheel`

Create source distribution: `python setup.py sdist`

And finally install locally: `pip install .`

## Run tests

Run all tests: `python -m unittest discover`

Notice: you need to select a region of screen to pass the tests.
