#!/bin/bash

# Set properties from the XML equivalent
freeCadPath="FreeCAD"
freeCadPatchSrc="freecad_patch.py"
a2plusRepo="https://github.com/kbwbe/A2plus"
a2plusVersion="0.4.26"

# OS-dependent variables
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Setting up environment for Linux..."
    freeCadRelease="https://github.com/FreeCAD/FreeCAD/releases/download/0.18.3/FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage"
    freeCadPathLinux="$freeCadPath/squashfs-root/usr"
    freeCadModLinux="$freeCadPathLinux/Mod"
    freeCadPatchDestLinux="$freeCadModLinux/Test/TestApp.py"
    a2plusPathLinux="$freeCadModLinux/A2plus"
    a2plusZipLinux="$freeCadModLinux/a2plus.zip"
    a2plusUnzippedLinux="$freeCadModLinux/A2plus-${a2plusVersion}"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Setting up environment for Windows..."
    freeCadRelease="https://github.com/FreeCAD/FreeCAD/releases/download/0.18.3/FreeCAD-0.18.16131.3129ae4-WIN-x64-portable.7z"
    freeCadPathWindows="FreeCAD"
    freeCadModWindows="$freeCadPathWindows/FreeCAD/Mod"
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

# Download FreeCAD if not already downloaded
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Checking if FreeCAD for Linux is already downloaded..."
    if [[ ! -f "$freeCadPath/AppImage" ]]; then
        echo "Downloading FreeCAD for Linux..."
        wget -O "$freeCadPath/AppImage" "$freeCadRelease"
        chmod +x "$freeCadPath/AppImage"
        echo "FreeCAD AppImage downloaded."
    else
        echo "FreeCAD AppImage already exists. Skipping download."
    fi

    # Extract FreeCAD AppImage if not already extracted
    if [[ ! -d "$freeCadPathLinux" ]]; then
        echo "Extracting FreeCAD AppImage..."
        ./"$freeCadPath/AppImage" --appimage-extract
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
    if [[ ! -d "$freeCadPath/FreeCAD" ]]; then
        echo "Extracting FreeCAD for Windows..."
        "C:/Program Files/7-Zip/7z.exe" x "$freeCadPath/FreeCAD.7z" -o"$freeCadPath/FreeCAD"
        echo "FreeCAD extracted successfully."
         # Move all the content from "$freeCadPath/FreeCAD/FreeCAD" to "$freeCadPath/FreeCAD"
        if [[ -d "$freeCadPath/FreeCAD/FreeCAD" ]]; then
            echo "Moving extracted files from $freeCadPath/FreeCAD/FreeCAD to $freeCadPath/FreeCAD"
            mv "$freeCadPath/FreeCAD/FreeCAD/"* "$freeCadPath/FreeCAD/"
            rm -rf "$freeCadPath/FreeCAD/FreeCAD"  # Clean up empty directory
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

# Check if A2plus is already downloaded
echo "Checking if A2plus is already downloaded..."
if [[ ! -f "$a2plusZipWindows" ]]; then
    echo "Downloading A2plus for Windows..."
    curl -L -o "$a2plusZipWindows" "$a2plusRepo/archive/v${a2plusVersion}.zip"
    echo "A2plus downloaded."
else
    echo "A2plus already downloaded. Skipping download."
fi


# Extract A2plus if not already extracted
if [[ ! -d "$a2plusUnzippedWindows" ]]; then
    echo "Extracting A2plus..."
    unzip -o "$a2plusZipWindows" -d "$a2plusPathWindows"  # Extract directly into the desired directory
    echo "A2plus extracted successfully."
else
    echo "A2plus already extracted. Skipping extraction."
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
    if [[ ! -f "$freeCadPathWindows/FreeCAD/bin/python.exe" ]]; then
        echo "Python executable not found! Check the FreeCAD installation."
        exit 1
    fi
    echo "Installing dependencies for Windows..."
    "$freeCadPathWindows/FreeCAD/bin/python.exe" -m pip install urllib3
fi

# Cleanup
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Cleaning up Linux..."
    rm "$freeCadPath/AppImage"
    rm "$a2plusZipLinux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Cleaning up Windows..."
    rm "$freeCadPathWindows/FreeCAD.7z"
    rm "$a2plusZipWindows"
fi

echo "Environment setup completed successfully."
