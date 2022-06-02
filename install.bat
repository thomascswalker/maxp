:start
cls

SET /p VERSION="Enter 3ds Max version: "
SET MAX_PYTHON="%ADSK_3DSMAX_x64_%%VERSION%Python\python.exe"
%MAX_PYTHON% -m ensurepip --default-pip
%MAX_PYTHON% -m pip --version
%MAX_PYTHON% -m pip install --upgrade pip setuptools wheel
%MAX_PYTHON% -m pip install --upgrade maxp