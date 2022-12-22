# Stellaris Mods Installer v1.3 by Ultra119

import shutil
import logging

from pathlib import Path

def get_root_path():
    # Returns the current working directory as a Path object.
    return Path.cwd()

def edit_mod(file_path: Path):
    # Copies the .mod file to the root directory and modifies its contents to include the full path of the original
    # .mod file in a new line at the end of the file.
    mod_file_copy_path = get_root_path() / (file_path.parent.name + '.mod')
    shutil.copy(str(file_path), str(mod_file_copy_path))

    with mod_file_copy_path.open("r+") as mod_file:
        # Delete the line that starts with path=, if it is present in the file
        lines = mod_file.readlines()
        mod_file.seek(0)
        for line in lines:
            if not line.startswith("path="):
                mod_file.write(line)
        mod_file.truncate()

        # Add a new line at the end of the file with the full path from which the file was copied
        mod_file.write("\n" + "path=" + '"' + str(file_path.parent).replace("\\", "/") + '"' + "\n")

    log(f"{file_path.parent} installed!", "info")

def unpack_archive(archive_path: Path):
    # Unpacks the specified archive to the root directory and returns a list of .mod files found in the unpacked
    # directory.
    if archive_path.suffix in ('.zip', '.rar'):
        log(f"{archive_path} is not a .mod, unpacking...", "info")
        shutil.unpack_archive(str(archive_path), str(get_root_path() / archive_path.stem))
        return [f for f in (get_root_path() / archive_path.stem).iterdir() if f.is_file() and f.suffix == '.mod']
    else:
        # log(f"{archive_path} is not a .zip or .rar archive", "warning")
        return []

def install_mod(mod_path: Path):
    # Installs the specified .mod file.
    if mod_path.suffix == '.mod':
        edit_mod(mod_path)
    else:
        log(f"{mod_path} is not a .mod file", "warning")

# Set up logging to a file and the console
logging.basicConfig(level=logging.INFO, filename='mod_installer.log', filemode='w', format='%(levelname)s: %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

def log(message: str, level: str):
    # Write the specified message to the log file and console with a prefix indicating the log level.
    if level == "info":
        logging.info(f"[{level.upper()}] {message}")
    elif level == "warning":
        logging.warning(f"[{level.upper()}] {message}")

def main():
    root_path = get_root_path()
    for path in root_path.iterdir():
        # Check if a .mod file with the same name as the directory or archive already exists in the root directory
        mod_file_path = root_path / (path.name + '.mod')
        if mod_file_path.exists():
            # Skip installing if a modded .mod file with the same name already exists in the root directory
            log(f"{mod_file_path} already exists, skipping installation", "info")
            continue

        if path.is_dir():
            # Check for .mod files in the directory
            mod_files = [f for f in path.iterdir() if f.is_file() and f.suffix == '.mod']
            for mod_file in mod_files:
                # Skip installing if a modded .mod file with the same name already exists in the root directory
                if (root_path / mod_file.name).exists():
                    log(f"{mod_file} already installed, skipping installation", "info")
                    continue
                install_mod(mod_file)

            # Check for archives in the directory and unpack them
            archive_files = [f for f in path.iterdir() if f.is_file() and f.suffix in ('.zip', '.rar')]
            for archive_file in archive_files:
                mod_files_unpacked = unpack_archive(archive_file)
                for mod_file_unpacked in mod_files_unpacked:
                    # Skip installing if a modded .mod file with the same name already exists in the root directory
                    if (root_path / mod_file_unpacked.name).exists():
                        log(f"{mod_file_unpacked} already installed, skipping installation", "info")
                        continue
                    install_mod(mod_file_unpacked)

        elif path.is_file():
            # Check if the file is an archive and unpack it
            if path.suffix in ('.zip', '.rar'):
                # Skip unpacking the archive if a modded .mod file with the same name already exists in the root directory
                if (root_path / path.stem).exists():
                    log(f"{path} already installed, skipping installation", "info")
                    continue
                mod_files_unpacked = unpack_archive(path)
                for mod_file_unpacked in mod_files_unpacked:
                    # Skip installing if a modded .mod file with the same name already exists in the root directory
                    if (root_path / mod_file_unpacked.name).exists():
                        log(f"{mod_file_unpacked} already installed, skipping installation", "info")
                        continue
                    install_mod(mod_file_unpacked)



main()

input("Press Enter to exit...")