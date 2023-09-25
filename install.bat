@echo off
echo Installing mipaquete...

:: Check if pip is installed
where pip >nul 2>nul
if errorlevel 1 (
    echo pip was not found, installing...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
)

:: Install your package
pip install gitmess==0.1.2

echo mipaquete has been successfully installed!

:: Define where gm.bat will be placed
set GM_PATH=%USERPROFILE%\AppData\Local\Programs\gm.bat

:: Ensure the gm command is globally available
:: This assumes that gitmess provides an executable named gm.exe after installation.
if not exist "%GM_PATH%" (
    echo @echo off > "%GM_PATH%"
    echo python -m gitmess %%* >> "%GM_PATH%"
    setx PATH "%PATH%;%USERPROFILE%\AppData\Local\Programs" /M
)

echo Script completed!
