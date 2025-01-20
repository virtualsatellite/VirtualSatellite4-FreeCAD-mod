#!/bin/bash

# Set properties from the XML equivalent
freeCadPath="FreeCAD"
freeCadPatchSrc="freecad_patch.py"
a2plusRepo="https://github.com/kbwbe/A2plus"
a2plusVersion="0.4.26"

# OS-dependent variables
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Setting up environment for Linux..."
    freeCadRelease="https://github.com/FreeCAD/FreeCAD/releases/download/0.21.0/FreeCAD_0.21.0-Linux-x86_64.AppImage"
    freeCadPathLinux="$freeCadPath/squashfs-root/usr"
    freeCadModLinux="$freeCadPathLinux/Mod"
    freeCadPatchDestLinux="$freeCadModLinux/Test/TestApp.py"
    a2plusPathLinux="A2plus"
    a2plusZipLinux="$a2plusPathLinux/a2plus.zip"
    a2plusUnzippedLinux="$a2plusPathLinux/A2plus-${a2plusVersion}"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Setting up environment for Windows..."
    freeCadRelease="https://github.com/FreeCAD/FreeCAD/releases/download/0.21.0/FreeCAD_0.21.0-Windows-x86_64.7z"
    freeCadModWindows="$freeCadPath/Mod"
    freeCadPatchDestWindows="$freeCadModWindows/Test/TestApp.py"
    a2plusPathWindows="A2plus" # path for A2plus
    a2plusZipWindows="$a2plusPathWindows/a2plus.zip"  # Path for A2plus ZIP file
    a2plusUnzippedWindows="$a2plusPathWindows/A2plus-${a2plusVersion}" # Path for the extracted folder
else
    echo "Unsupported operating system!"
    exit 1
fi

# Check for 7z on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Add 7z to PATH if it's not found in the environment
    if ! command -v 7z &> /dev/null; then
        echo "7z command not found. Trying to add it to PATH..."
        export PATH="$PATH:/c/Program Files/7-Zip"
        
        # Check again after adding to PATH
        if ! command -v 7z &> /dev/null; then
            echo "7z command still not found. Please install 7-Zip (https://www.7-zip.org/)"
            exit 1
        fi
    fi
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Check if FreeCAD directory exists, if not, create it
    if [[ ! -d "$freeCadPath" ]]; then
        echo "Directory $freeCadPath does not exist. Creating it..."
        mkdir -p "$freeCadPath"
        echo "Directory $freeCadPath created."
    fi
    
    # Check if FreeCAD AppImage is already downloaded
    echo "Checking if FreeCAD for Linux is already downloaded..."
     if ! find "$freeCadPath" -maxdepth 1 -type f -name "*.AppImage" | grep -q .; then
        echo "No .AppImage file found. Downloading FreeCAD for Linux..."
        wget -O "$freeCadPath/FreeCAD.AppImage" "$freeCadRelease"
        chmod +x "$freeCadPath/FreeCAD.AppImage"
        echo "FreeCAD AppImage downloaded and made executable."
    else
        echo "An .AppImage file already exists. Skipping download."
    fi


    if [[ ! -d "$freeCadPathLinux" ]]; then
        echo "Extracting FreeCAD AppImage..."
        "$freeCadPath/FreeCAD.AppImage" --appimage-extract  # Use full path to AppImage
        mv "squashfs-root" "$freeCadPath"  # Move extracted contents into the desired directory
        echo "FreeCAD extracted successfully."
    else
        echo "FreeCAD already extracted. Skipping extraction."
    fi


elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Checking if FreeCAD for Windows is already downloaded and extracted..."

    # Check if the folder exists and is not empty
    if [[ -d "$freeCadPath/FreeCAD" && "$(ls -A "$freeCadPath/FreeCAD")" ]]; then
        echo "FreeCAD folder exists and is not empty. Skipping download."
    elif [[ ! -d "$freeCadPath/FreeCAD" && -f "$freeCadPath/FreeCAD.7z" ]]; then
        echo "FreeCAD folder is missing, but 7z file exists. Skipping download."
    else
        # If folder is missing or empty and 7z file is not present, download the archive
        echo "FreeCAD folder is missing or empty, and 7z file is not found. Downloading FreeCAD for Windows..."
        curl -L -o "$freeCadPath/FreeCAD.7z" "$freeCadRelease"
        echo "FreeCAD 7z archive downloaded."
    fi


    # Extract FreeCAD for Windows if not already extracted
    if [[ ! -d "$freeCadPath/bin" ]]; then
        echo "Extracting FreeCAD for Windows..."
        "C:/Program Files/7-Zip/7z.exe" x "$freeCadPath/FreeCAD.7z" -o"$freeCadPath/FreeCAD"
        echo "FreeCAD extracted successfully."
         # Move all the content from "$freeCadPath/FreeCAD/FreeCAD" to "$freeCadPath/FreeCAD"
        if [[ -d "$freeCadPath/FreeCAD" ]]; then
            echo "Moving extracted files from $freeCadPath/FreeCAD/* to $freeCadPath"
            mv "$freeCadPath"/FreeCAD/*/* "$freeCadPath/"
            sleep 5
            rm -rf "$freeCadPath/FreeCAD"  # Clean up empty directory
            echo "Files moved successfully."
        else
            echo "Error: Extracted FreeCAD directory not found."
        fi
    else
        echo "FreeCAD already extracted. Skipping extraction."
    fi
fi

# Ensure directories exist before proceeding
if [[ ! -d "$freeCadModWindows" && "$OSTYPE" == "msys" ]]; then
    echo "Directory $freeCadModWindows does not exist! Exiting."
    exit 1
fi

# Linux-specific A2plus download and extraction
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Ensure A2plus directory exists
    if [[ ! -d "$a2plusPathLinux" ]]; then
        echo "Directory $a2plusPathLinux does not exist. Creating it..."
        mkdir -p "$a2plusPathLinux"
        echo "Directory $a2plusPathLinux created."
    fi

    # Check if A2plus is already downloaded
    echo "Checking if A2plus is already downloaded for Linux..."
    if [[ ! -f "$a2plusZipLinux" ]]; then
        echo "Downloading A2plus for Linux..."
        curl -L -o "$a2plusZipLinux" "${a2plusRepo}/archive/v${a2plusVersion}.zip"
        echo "A2plus downloaded."
    else
        echo "A2plus already downloaded. Skipping download."
    fi


    # Extract A2plus if not already extracted
    if [[ ! -d "$a2plusUnzippedLinux" ]]; then
        echo "Extracting A2plus for Linux..."
        unzip -o "$a2plusZipLinux" -d "$a2plusPathLinux"  # Extract directly into the desired directory
        echo "A2plus extracted successfully."
    else
        echo "A2plus already extracted. Skipping extraction."
    fi

    # Moving A2PLus Module to FreeCAD Mod if not done
    if [[ ! -d "$freeCadModLinux"/A2plus ]]; then
        echo "Moving the A2plus module"
        mv "$a2plusUnzippedLinux" "$freeCadModLinux"/A2plus
        echo "A2plus moved successfully."
    else
        echo "A2plus already available. Skipping the step."
    fi

fi


# Windows-specific A2plus download and extraction
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Check if A2plus is already downloaded
    echo "Checking if A2plus is already downloaded for Windows..."
    if [[ ! -f "$a2plusZipWindows" ]]; then
        echo "Downloading A2plus for Windows..."
        curl -L -o "$a2plusZipWindows" "$a2plusRepo/archive/v${a2plusVersion}.zip"
        echo "A2plus downloaded."
    else
        echo "A2plus already downloaded. Skipping download."
    fi

    # Extract A2plus if not already extracted
    if [[ ! -d "$a2plusUnzippedWindows" ]]; then
        echo "Extracting A2plus for Windows..."
        unzip -o "$a2plusZipWindows" -d "$a2plusPathWindows"  # Extract directly into the desired directory
        echo "A2plus extracted successfully."
    else
        echo "A2plus already extracted. Skipping extraction."
    fi

fi

# Apply patch
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Applying patch to FreeCAD for Linux..."
    cp "$freeCadPatchSrc" "$freeCadPatchDestLinux"
    echo "Patch applied successfully."
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Applying patch to FreeCAD for Windows..."
    cp "$freeCadPatchSrc" "$freeCadPatchDestWindows"
    echo "Patch applied successfully."
fi

# Install dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing dependencies for Linux..."
    "$freeCadPathLinux/bin/python" -m pip install urllib3
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    if [[ ! -f "$freeCadPath/bin/python.exe" ]]; then
        echo "Python executable not found! Check the FreeCAD installation."
        exit 1
    fi
    echo "Installing dependencies for Windows..."
    "$freeCadPath/bin/python.exe" -m pip install urllib3
fi

# Cleanup
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Cleaning up Linux..."
    rm "$freeCadPath/FreeCAD.AppImage"
    rm "$a2plusZipLinux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Cleaning up Windows..."
    rm "$freeCadPath/FreeCAD.7z"
    rm "$a2plusZipWindows"
fi

echo "Environment setup completed successfully."
