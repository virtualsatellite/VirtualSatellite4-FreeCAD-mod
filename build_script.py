import os
import shutil
import subprocess
import requests
from pathlib import Path

def ensure_directory(path):
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path, exist_ok=True)

def download_file(url, destination):
    print(f"Downloading from {url} to {destination}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {destination}")
    else:
        print(f"Failed to download {url}")
        response.raise_for_status()

def extract_7z(archive_path, extract_to, seven_zip_path):
    print(f"Extracting {archive_path} to {extract_to}")
    result = subprocess.run(
        [seven_zip_path, "x", archive_path, f"-o{extract_to}", "-aoa"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Extraction failed: {result.stderr}")
        raise Exception("7z extraction failed")
    print("Extraction completed.")

def move_contents(src_dir, dest_dir):
    print(f"Moving contents from {src_dir} to {dest_dir}")
    move_failed = False
    for item in Path(src_dir).iterdir():
        try:
            shutil.move(str(item), dest_dir)
            print(f"Moved: {item}")
        except Exception as e:
            print(f"Failed to move {item}: {e}")
            move_failed = True
    if move_failed:
        raise Exception("Some files could not be moved.")

def main():
    # Paths
    script_dir = Path(__file__).parent
    freecad_dir = script_dir / "FreeCAD"
    a2plus_dir = script_dir / "A2plus"
    seven_zip_path = script_dir / "tools" / "7zip" / "7z.exe"
    freecad_archive = freecad_dir / "FreeCAD.7z"
    extracted_freecad_dir = freecad_dir

    # Ensure directories exist
    ensure_directory(freecad_dir)
    ensure_directory(a2plus_dir)

    # Check if FreeCAD is already extracted
    if (freecad_dir / "bin" / "python.exe").exists():
        print("FreeCAD is already extracted and available. Skipping download and extraction.")
    else:
        # Download FreeCAD if it doesn't exist
        if not freecad_archive.exists():
            freecad_url = "https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Windows-x86_64.7z"
            download_file(freecad_url, freecad_archive)
        else:
            print("FreeCAD archive already exists. Skipping download.")

        # Extract FreeCAD
        extract_7z(freecad_archive, extracted_freecad_dir, seven_zip_path)

        # Identify the extracted directory
        extracted_dirs = list(freecad_dir.glob("FreeCAD_*"))
        if not extracted_dirs:
            print("Failed to find the extracted FreeCAD directory.")
            print(f"Contents of {freecad_dir}: {list(freecad_dir.iterdir())}")
            return

        new_freecad_dir = extracted_dirs[0]
        print(f"Identified extracted directory: {new_freecad_dir}")

        # Move contents
        move_contents(new_freecad_dir, freecad_dir)

        # Delete the extracted directory
        shutil.rmtree(new_freecad_dir)
        print(f"Deleted directory: {new_freecad_dir}")

    # Check Python executable
    if not (freecad_dir / "bin" / "python.exe").exists():
        print("Python executable not found. Please check the extraction process.")
        return

    # Download A2plus if it doesn't exist
    a2plus_zip = a2plus_dir / "a2plus.zip"
    if not a2plus_zip.exists():
        a2plus_url = "https://github.com/kbwbe/A2plus/archive/v0.4.26.zip"
        download_file(a2plus_url, a2plus_zip)
    else:
        print("A2plus archive already exists. Skipping download.")

    # Extract A2plus
    extract_7z(a2plus_zip, a2plus_dir, seven_zip_path)

    # Install Python dependencies
    print("Installing Python dependencies...")
    result = subprocess.run(
        [str(freecad_dir / "bin" / "python.exe"), "-m", "pip", "install", "urllib3"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Failed to install Python dependencies: {result.stderr}")
        return

    print("Setup completed successfully.")

if __name__ == "__main__":
    main()
