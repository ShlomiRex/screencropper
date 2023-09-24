# How to test

First create virtual environment:

```bash
cd tests
python3 -m venv venv
source venv/bin/activate
```

Or on windows:
```powershell
cd tests
python -m venv venv
venv\Scripts\activate
```

Then install the package (from the `tests` directory): `pip install ..`

Then run the tests: `python -m unittest discover`