REM Variables
SET max_python="C:\Program Files\Autodesk\3ds Max 2022\Python37\python.exe"
SET max_packages="C:\Program Files\Autodesk\3ds Max 2022\Python37\Lib\site-packages\"

set venv_path=%userprofile%\.venv
set bettermaxtools=%cd%

py -m pip install --upgrade build
py -m build

REM Create the venv
%max_python% -m virtualenv %venv_path%
cd %venv_path%\Scripts

REM Activate the venv
call .\activate.bat

REM install packages
py -m pip install %bettermaxtools%\dist\*


