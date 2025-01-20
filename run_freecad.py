import subprocess
import os
import sys

print(os.getcwd())
current_dir=os.getcwd()
# Base path to the FreeCAD executable
freecad_dir = os.path.join(current_dir, "FreeCAD/squashfs-root/usr/bin")
freecad_executable = os.path.join(freecad_dir,"freecad")

# Base arguments (common ones can be set here)
base_args = [
   freecad_executable
]

# Collect additional arguments from command-line inputs (if provided)
additional_args = sys.argv[1:]

# Combine all arguments
args = base_args + additional_args

# Log the full command for debugging
print(f"Running command: {' '.join(args)}")

# Run the FreeCAD executable with the given arguments
subprocess.run(args)
