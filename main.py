# Stellaris Mods Installer v1.0 by Ultra119

import os
import shutil

# Get the path to the folder from which the script was launched
root = os.getcwd()

# Get a list of all folders in the root
folders = os.listdir(root)

# For each folder in the root
for folder in folders:
    # Get the full path to the folder and convert \ to /
    folder_path = os.path.join(root, folder).replace("\\", "/")

    # If the folder is a directory
    if os.path.isdir(folder_path):
        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)
            file_ext = os.path.splitext(file_path)[1]

            # If the file extension is .mod
            if file_ext == ".mod":
                if os.path.exists(os.path.join(root, folder + ".mod")):
                    print(folder + ".mod already exists")
                    break
                else:
                    # Copy the file to the folder in which the script is located
                    shutil.copy(file_path, root)

                # Rename the copied file to the name of the folder from which it was originally copied
                shutil.move(os.path.join(root, file), os.path.join(root, folder + ".mod"))

                # Get the full path to the renamed file
                renamed_file_path = os.path.join(root, folder + ".mod")
                with open(renamed_file_path, "r+") as mod_file:
                    # Delete the line that starts with path=, if it is present in the file
                    lines = mod_file.readlines()
                    mod_file.seek(0)
                    
                    for line in lines:
                        if not line.startswith("path="):
                            mod_file.write(line)
                    mod_file.truncate()

                    # Add a new line at the end of the file with the full path from which the file was copied
                    mod_file.write("\n" + "path=" + '"' + folder_path + '"' + "\n")

                print("Installed " + folder_path)

            elif file_ext == ".zip" and ".rar":
                print("ERROR: " + file_path.replace("/", "\\") + " is not a .mod, unpack it and run script again")
                break

            else:
                pass

    else:
        pass

input("Press Enter to exit...")
exit()
