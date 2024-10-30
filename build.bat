@echo off
setlocal

REM Set paths
set "FREECAD_DIR=C:\git\VirtualSatellite4-FreeCAD-mod\FreeCAD"
set "A2PLUS_DIR=C:\git\VirtualSatellite4-FreeCAD-mod\A2plus"  REM Ensure this directory exists
mkdir "%A2PLUS_DIR%"   REM Creating Directory if not existing
set "SEVEN_ZIP_PATH=C:\Program Files\7-Zip\7z.exe"  REM Ensure this path is correct
set "FREECAD_ARCHIVE=%FREECAD_DIR%\FreeCAD.7z" 
set "EXTRACTED_FREECAD_DIR=%FREECAD_DIR%"  REM Directory where FreeCAD is extracted

REM Create directories if they do not exist
mkdir "%FREECAD_DIR%"

REM Check if FreeCAD is already extracted by checking if python.exe exists
if exist "%FREECAD_DIR%\bin\python.exe" (
    echo FreeCAD is already extracted and available. Skipping download and extraction.
    goto :check_a2plus
)

REM Download FreeCAD if it doesn't exist
if not exist "%FREECAD_ARCHIVE%" (
    echo Downloading FreeCAD...
    curl -L -o "%FREECAD_ARCHIVE%" "https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Windows-x86_64.7z"
    if ERRORLEVEL 1 (
        echo Failed to download FreeCAD.
        exit /b
    )
) else (
    echo FreeCAD archive already exists. Skipping download.
)

REM Extract FreeCAD
if exist "%FREECAD_ARCHIVE%" (
    echo Extracting FreeCAD...
    "%SEVEN_ZIP_PATH%" x "%FREECAD_ARCHIVE%" -o"%EXTRACTED_FREECAD_DIR%"
    if ERRORLEVEL 1 (
        echo Failed to extract FreeCAD.
        exit /b
    )
)

REM Identify the extracted FreeCAD directory
set "NEW_FREECAD_DIR="
for /d %%F in ("%FREECAD_DIR%\FreeCAD_*") do (
    set "NEW_FREECAD_DIR=%%F"
)

REM Check if the new FreeCAD directory was found
if not defined NEW_FREECAD_DIR (
    echo Failed to find the extracted FreeCAD directory.
    echo Checking contents of "%FREECAD_DIR%":
    dir "%FREECAD_DIR%"
    exit /b
)

REM Move the contents of the FreeCAD directory to the main directory
echo Moving contents of the FreeCAD directory to the main directory...
set "MOVE_FAILED=0"

for /d %%F in ("%NEW_FREECAD_DIR%\*") do (
    echo Attempting to move directory "%%F" to "%FREECAD_DIR%"
    move "%%F" "%FREECAD_DIR%"
    if ERRORLEVEL 1 (
        echo Failed to move "%%F".
        set "MOVE_FAILED=1"
    ) else (
        echo Successfully moved "%%F".
    )
)

for %%F in ("%NEW_FREECAD_DIR%\*") do (
    echo Attempting to move file "%%F" to "%FREECAD_DIR%"
    move "%%F" "%FREECAD_DIR%"
    if ERRORLEVEL 1 (
        echo Failed to move "%%F".
        set "MOVE_FAILED=1"
    ) else (
        echo Successfully moved "%%F".
    )
)

if %MOVE_FAILED%==1 (
    echo Some files could not be moved. Please check the log above.
    exit /b
)

REM Delete the extracted FreeCAD directory
echo Deleting extracted FreeCAD directory...
rmdir /S /Q "%NEW_FREECAD_DIR%"
if ERRORLEVEL 1 (
    echo Failed to delete the directory "%NEW_FREECAD_DIR%".
) else (
    echo Successfully deleted the directory "%NEW_FREECAD_DIR%".
)

REM Check if Python exists in the extracted FreeCAD directory
if not exist "%FREECAD_DIR%\bin\python.exe" (
    echo Python executable not found in %FREECAD_DIR%\bin.
    echo Please check the extraction process.
    exit /b
)

:check_a2plus

REM Download A2plus if it doesn't exist
if not exist "%A2PLUS_DIR%\a2plus.zip" (
    echo Downloading A2plus...
    curl -L -o "%A2PLUS_DIR%\a2plus.zip" "https://github.com/kbwbe/A2plus/archive/v0.4.26.zip"
    if ERRORLEVEL 1 (
        echo Failed to download A2plus.
        exit /b
    )
) else (
    echo A2plus already downloaded. Skipping download.
)

REM Extract A2plus
if exist "%A2PLUS_DIR%\a2plus.zip" (
    echo Extracting A2plus...
    "%SEVEN_ZIP_PATH%" x "%A2PLUS_DIR%\a2plus.zip" -o"%A2PLUS_DIR%" -aoa
    if ERRORLEVEL 1 (
        echo Failed to extract A2plus.
        exit /b
    )
)

REM Install Python dependencies
echo Installing Python dependencies...
"%FREECAD_DIR%\bin\python.exe" -m pip install urllib3
if ERRORLEVEL 1 (
    echo Failed to install Python dependencies.
    exit /b
)

echo Setup completed successfully.
endlocal
