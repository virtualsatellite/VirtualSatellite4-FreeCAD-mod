import subprocess
import os
import sys
import platform

# Get the current working directory
print(os.getcwd())
current_dir = os.getcwd()

# Detect the operating system
def is_windows():
    return os.name == 'nt' or platform.system().lower() == 'windows'

def is_linux():
    return os.name == 'posix' or platform.system().lower() == 'linux'

if is_linux():
    # Linux-specific FreeCAD path
    freecad_dir = os.path.join(current_dir, "FreeCAD/squashfs-root/usr/bin")
    freecad_executable = os.path.join(freecad_dir, "freecad")

    # Base arguments
    base_args = [
        freecad_executable
    ]

elif is_windows():
    # Windows-specific FreeCAD path
    freecad_path = os.path.join(current_dir, "FreeCAD/bin/FreeCAD.exe")

    # Base arguments
    base_args = [
        freecad_path
    ]
else:
    print("Unsupported operating system.")
    sys.exit(1)

# Collect additional arguments from command-line inputs (if provided)
additional_args = sys.argv[1:]

# Combine all arguments
args = base_args + additional_args

# Log the full command for debugging
print(f"Running command: {' '.join(args)}")

# Run the FreeCAD executable with the given arguments
subprocess.run(args)
