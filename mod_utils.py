import shutil
import logging
import os

from pathlib import Path


def log(message: str, level: str):
    # Write the specified message to the log file and console with a prefix indicating the log level.
    if level == "info":
        logging.info(f"[{level.upper()}] {message}")
    elif level == "warning":
        logging.warning(f"[{level.upper()}] {message}")
        
        
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
    if mod_path.suffix != '.mod':
        log(f"{mod_path} is not a .mod file", "warning")
        return

    mod_file_copy_path = get_root_path() / f"{mod_path.parent.name}.mod"
    if mod_file_copy_path.exists():
        user_input = input(f"Mod with name '{mod_path.parent.name}' already exists in the root directory. "
                           "Enter 'O' to overwrite or 'S' to skip: ").upper()
        if user_input == 'S':
            log(f"Installation of mod '{mod_path.parent.name}' skipped by user.", "info")
            return
        elif user_input != 'O':
            log(f"Invalid input: {user_input}", "warning")
            install_mod(mod_path)
            return
        try:
            os.remove(str(mod_file_copy_path))
        except Exception as e:
            log(f"Error removing existing mod: {e}", "warning")
            return
    try:
        edit_mod(mod_path)
    except Exception as e:
        log(f"Error installing mod: {e}", "warning")
