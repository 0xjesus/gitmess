@echo off
echo Installing mipaquete...

:: Check if pip is installed
where pip >nul 2>nul
if errorlevel 1 (
    echo pip was not found, installing...
    :: Note: Installing pip this way is a simplification. You might want to provide more detailed instructions or a different method.
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
)

:: Install your package
pip install gitmess==0.1.0

echo mipaquete has been successfully installed!

:: Ensure the gm command is globally available
:: This assumes that gitmess provides an executable named gm.exe after installation.
if not exist "%USERPROFILE%\gm.bat" (
    echo @echo off > "%USERPROFILE%\gm.bat"
    echo python -m gitmess %%* >> "%USERPROFILE%\gm.bat"
    setx PATH "%PATH%;%USERPROFILE%" /M
)

echo Script completed!
