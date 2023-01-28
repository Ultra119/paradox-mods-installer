# Stellaris Mods Installer v1.4 by Ultra119

import shutil
import logging
import os

from pathlib import Path


def get_root_path():
    # Returns the current working directory as a Path object.
    return Path.cwd()


def edit_mod(file_path: Path):
    # Copies the .mod file to the root directory and modifies its contents to include the full path of the original
    # .mod file in a new line at the end of the file.
    mod_file_copy_path = get_root_path() / (file_path.parent.name + '.mod')
    shutil.copy(str(file_path), str(mod_file_copy_path))

    try:
        with mod_file_copy_path.open("r+") as mod_file:
            # Extract the mod name from the 'name' field in the mod file
            lines = mod_file.readlines()
            mod_name = None
            for line in lines:
                if line.startswith("name="):
                    mod_name = line.split("=")[1].strip()
                    break

            # Delete the line that starts with path=, if it is present in the file
            mod_file.seek(0)
            for line in lines:
                if not line.startswith("path="):
                    mod_file.write(line)
            mod_file.truncate()

            # Add a new line at the end of the file with the full path from which the file was copied
            mod_file.write("\n" + "path=" + '"' + str(file_path.parent).replace("\\", "/") + '"' + "\n")
    except IOError as e:
        log(f"Error opening mod file: {e}", "warning")
        return

    # Log the name of the installed mod
    if mod_name is not None:
        log(f"{mod_name} installed!", "info")


def unpack_archive(archive_path: Path):
    # Unpacks the specified archive to the root directory and returns a list of .mod files found in the unpacked
    # directory.
    if archive_path.suffix in ('.zip', '.rar'):
        log(f"{archive_path} is not a .mod, unpacking...", "info")
        try:
            shutil.unpack_archive(str(archive_path), str(get_root_path() / archive_path.stem))
        except Exception as e:
            log(f"Error unpacking archive: {e}", "warning")
            return []
        return [f for f in (get_root_path() / archive_path.stem).iterdir() if f.is_file() and f.suffix == '.mod']
    else:
        # log(f"{archive_path} is not a .zip or .rar archive", "warning")
        return []


def install_mod(mod_path: Path):
    # Installs the specified .mod file.
    if mod_path.suffix == '.mod':
        mod_file_copy_path = get_root_path() / (mod_path.parent.name + '.mod')
        if mod_file_copy_path.exists():
            # Mod with same name already exists in root directory
            while True:
                try:
                    user_input = input(f"Mod with name '{mod_path.parent.name}' already exists in the root directory. "
                                   "Enter 'O' to overwrite or 'S' to skip: ")
                    if user_input.upper() == "O":
                        try:
                            # Overwrite existing mod
                            os.remove(str(mod_file_copy_path))
                            edit_mod(mod_path)
                            break
                        except Exception as e:
                            log(f"Error installing mod: {e}", "warning")
                    elif user_input.upper() == "S":
                        log(f"Installation of mod '{mod_path.parent.name}' skipped by user.", "info")
                        break
                    else:
                        log(f"Invalid input: {user_input}", "warning")
                except Exception as e:
                    log(f"Error: {e}", "warning")
        else:
            try:
                edit_mod(mod_path)
            except Exception as e:
                log(f"Error installing mod: {e}", "warning")
    else:
        log(f"{mod_path} is not a .mod file", "warning")


# Set up logging to a file and the console
logging.basicConfig(level=logging.INFO, filename='mod_installer.log', filemode='w',
                    format='%(levelname)s: %(message)s (%(name)s)')
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
    try:
        # Print instructions to the user
        global mod_file_unpacked
        print("Welcome to the Stellaris Mods Installer!")
        print("Enter 'I' to install all mods")
        print("Enter 'V' to view installed mods")
        print("Enter 'Q' to quit")

        # Prompt the user for input
        user_input = input("Enter your selection: ")
        root_path = get_root_path()

        # Install all mods
        if user_input.upper() == "I":
            log("Installing all mods...", "info")
            for path in root_path.iterdir():
                # Check if a .mod file with the same name as the directory or archive already exists in the root directory
                mod_file_path = root_path / (path.name + '.mod')
                if mod_file_path.exists() and not root_path / path.name / (path.name + '.mod'):
                    # Skip installing if a modded .mod file with the same name already exists in the root directory
                    # and not in the mod directory
                    log(f"{mod_file_path} already exists, skipping installation", "info")
                    continue

                elif path.is_dir():
                    # Check for .mod files in the directory
                    mod_files = [f for f in path.iterdir() if f.is_file() and f.suffix == '.mod']
                    for mod_file in mod_files:
                        # Skip installing if a modded .mod file with the same name already exists in the root directory
                        if (root_path / mod_file.name).exists():
                            log(f"{mod_file} already installed, skipping installation", "info")
                            continue

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
                # Install the mod
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

            log("All mods installed!\n", "info")
            input("Press Enter to continue...")
            os.system('cls')
            main()

        # View installed mods
        elif user_input.upper() == "V":
            log("Viewing installed mods...", "info")
            # Iterate through the .mod files in the root directory
            counter = 1
            for path in root_path.iterdir():
                if path.suffix == '.mod':
                    # Extract the mod name and full path from the mod file
                    with path.open("r") as mod_file:
                        lines = mod_file.readlines()
                        mod_name = None
                        mod_path = None
                        for line in lines:
                            if line.startswith("name="):
                                mod_name = line.split("=")[1].strip()
                            elif line.startswith("path="):
                                mod_path = line.split("=")[1].strip()
                    # Print the mod number, name, and full path
                    print(f"{counter}. {mod_name} ({mod_path})")
                    counter += 1

            input("Press Enter to return...")
            os.system('cls')
            main()

        # Quit
        elif user_input.upper() == "Q":
            log("Exiting...", "info")
            exit()
        else:
            input("Invalid option. Press Enter to continue...")
            os.system('cls')
            main()

    except ValueError as e:
        log(str(e), "warning")

main()
