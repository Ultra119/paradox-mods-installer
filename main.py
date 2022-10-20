# Stellaris Mods Installer v1.2 by Ultra119

import shutil

from pathlib import Path

def get_root_path():
    return Path.cwd()

def edit_mod(file_path: Path):
    path_to_copy = get_root_path() / (file_path.parent.name + '.mod')
    shutil.copy(str(file_path), str(path_to_copy))

    with path_to_copy.open("r+") as mod_file:
        # Delete the line that starts with path=, if it is present in the file
        lines = mod_file.readlines()
        mod_file.seek(0)
        for line in lines:
            if not line.startswith("path="):
                mod_file.write(line)
        mod_file.truncate()

        # Add a new line at the end of the file with the full path from which the file was copied
        mod_file.write("\n" + "path=" + '"' + str(file_path.parent).replace("\\", "/") + '"' + "\n")

    print("INFO: " + str(file_path.parent) + " installed!")

def main():
    root_path = get_root_path()
    for mod_folder_path in root_path.iterdir():
        path_file_mod = root_path / (mod_folder_path.name + '.mod')
        if path_file_mod.exists():
            print("INFO: " + str(path_file_mod) + " already exists")
            continue
        else:
            if mod_folder_path.is_dir():
                # print(mod_folder_path)
                files = [f for f in mod_folder_path.iterdir() if f.is_file()]
                for file in files:
                    if file.suffix == '.mod':
                        edit_mod(file)
                    elif file.suffix in ('.zip', '.rar'):
                        if not [i for i in mod_folder_path.glob('*.mod')]:
                            print("INFO: " + str(file) + " is not a .mod, unpacking...")
                            shutil.unpack_archive(str(file), str(mod_folder_path))
                            files_new = [f for f in mod_folder_path.iterdir() if
                                         f.is_file() and f.suffix == '.mod']
                            for file_unpacked in files_new:
                                edit_mod(file_unpacked)

                        else:
                            print("INFO: " + str(file) + " is already unpacked")
                            continue


            elif mod_folder_path.is_file():
                if mod_folder_path.suffix in ('.zip', '.rar'):
                    if not (root_path / (mod_folder_path.stem + '.mod')).exists():
                        print("INFO: " + str(mod_folder_path) + " is not a .mod, unpacking...")
                        shutil.unpack_archive(str(mod_folder_path), str(root_path / mod_folder_path.stem))
                        files_new = [f for f in (root_path / mod_folder_path.stem).iterdir() if
                                        f.is_file() and f.suffix == '.mod']
                        for file_unpacked in files_new:
                            edit_mod(file_unpacked)
                            
                    else:
                        print("INFO: " + str(mod_folder_path) + " is already unpacked")
                        continue
main()

input("Press Enter to exit...")
