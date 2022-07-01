from distutils.util import convert_path
import os
import sys


macro_placement = "test text"
top_path="./"

# Copy starting here
macro_placement_path = top_path + "macro_placement.cfg"

if(os.path.exists(macro_placement_path)):
    rem = input('\nExisting macro_placement.cfg found on given path. Do you want to overwrite it? Type yes or no\n > ')
    if(rem == "yes"):
        os.remove(macro_placement_path)
    else:
        print("Aborting...")
        sys.exit()

# Write to the file
macro_file = open(macro_placement_path, "w")
macro_file.write(macro_placement)
print("Successfully wrote to macro_placement.cfg")