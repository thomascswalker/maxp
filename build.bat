@echo off
@RD /S /Q dist
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
python -m twine upload dist/* --verbose
