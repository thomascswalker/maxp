:start
cls

SET MAX_PYTHON="%ADSK_3DSMAX_x64_2023%Python\python.exe"
%MAX_PYTHON% -m ensurepip --default-pip
%MAX_PYTHON% -m pip --version
%MAX_PYTHON% -m pip install --upgrade maxp