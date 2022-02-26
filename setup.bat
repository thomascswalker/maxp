set venv_name=maxdev
set max_python=C:\"Program Files"\Autodesk\"3ds Max 2022"\Python37\python.exe
set max_packages=C:\"Program Files"\Autodesk\"3ds Max 2022"\Python37\Lib\site-packages\

@echo "Installing virtualenv..."
%max_python% -m ensurepip --upgrade
%max_python% -m pip install virtualenv
%max_python% -m pip install pyside2==5.15.1

popd

@pause