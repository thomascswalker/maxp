@echo off
:: Only support back to 3ds Max 2021
SET MAX_2021_PYTHON="%ADSK_3DSMAX_x64_2021%Python37\python.exe"
SET MAX_2022_PYTHON="%ADSK_3DSMAX_x64_2022%Python37\python.exe"
SET MAX_2023_PYTHON="%ADSK_3DSMAX_x64_2023%Python\python.exe"

:: Install 2021
if exist %MAX_2021_PYTHON% (
    CALL :Install %MAX_2021_PYTHON%
)

:: Install 2022
if exist %MAX_2022_PYTHON% (
    CALL :Install %MAX_2022_PYTHON%
)

:: Install 2023
if exist %MAX_2023_PYTHON% (
    CALL :Install %MAX_2023_PYTHON%
)

ECHO All versions installed or upgraded
set/p<nul =Press any key to exit...&pause>nul
EXIT /B %ERRORLEVEL%

:: Do the actual installation
:Install
ECHO Installing in %~1
"%~1" -m ensurepip --default-pip
"%~1" -m pip --version
"%~1" -m pip install --upgrade pip setuptools wheel
"%~1" -m pip install -e .
ECHO Installed in %~1
EXIT /B 0