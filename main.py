# Stellaris Mods Installer v1.1 by Ultra119

import os
import shutil


# Get the path to the folder from which the script was launched
root_path = os.getcwd()

# Get a list of all folders in the root
root_folders = os.listdir(root_path)

# For each folder in the root
for mod_folder_name in root_folders:
    # Get the full path to the folder
    mod_folder_path = os.path.join(root_path, mod_folder_name)

    # If the folder is a directory
    if os.path.isdir(mod_folder_path):
        mod_files = os.listdir(mod_folder_path)

        for file in mod_files:
            file_path = os.path.join(mod_folder_path, file)
            file_ext = os.path.splitext(file_path)[1]

            # If the file extension is .mod
            if file_ext == ".mod":
                if os.path.exists(os.path.join(root_path, mod_folder_name + ".mod")):
                    print("INFO: " + mod_folder_path + ".mod already exists")
                    break
                else:
                    # Copy the file to the folder in which the script is located
                    shutil.copy(file_path, root_path)

                # Rename the copied file to the name of the folder from which it was originally copied
                shutil.move(os.path.join(root_path, file), os.path.join(root_path, mod_folder_name + ".mod"))

                # Get the full path to the renamed file
                renamed_file_path = os.path.join(root_path, mod_folder_name + ".mod")
                with open(renamed_file_path, "r+") as mod_file:
                    # Delete the line that starts with path=, if it is present in the file
                    lines = mod_file.readlines()
                    mod_file.seek(0)
                    for line in lines:
                        if not line.startswith("path="):
                            mod_file.write(line)
                    mod_file.truncate()

                    # Add a new line at the end of the file with the full path from which the file was copied
                    mod_file.write("\n" + "path=" + '"' + mod_folder_path + '"' + "\n")

                print("INFO: " + mod_folder_path + " installed!")

            elif file_ext == ".zip" and ".rar":
                print("ERROR: " + file_path + " is not a .mod, unpack it and run script again")
                break

            else:
                pass

    else:
        pass

input("Press Enter to exit...")
exit()
