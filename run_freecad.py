import subprocess
import os
import sys

print(os.getcwd())
# Base path to the FreeCAD executable
freecad_path = os.path.join(os.getcwd(), "FreeCAD/bin/FreeCAD.exe")

# Base arguments (common ones can be set here)
base_args = [
    freecad_path,
]

# Collect additional arguments from command-line inputs (if provided)
additional_args = sys.argv[1:]

# Combine all arguments
args = base_args + additional_args

# Log the full command for debugging
print(f"Running command: {' '.join(args)}")

# Run the FreeCAD executable with the given arguments
subprocess.run(args)
