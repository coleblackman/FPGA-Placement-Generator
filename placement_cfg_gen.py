# Ask for project directory
import sys
import os

if len(sys.argv) > 1:
    top_path = sys.argv[1]
    print("\n\033[1;32mProject\033[m location supplied as a script argument: \033[1;32m", top_path, "\033[m")
else:
    top_path = input('Input location of \033[1;32mproject\033[m, type \"local\" for local directory, or type \"default\" for default.\n> ')
    if top_path == "default" or top_path == "":
        top_path = '.'
# Set paths for config.tcl, macro_placement.cfg
config_tcl_path = top_path + "config.tcl"
macro_placement_cfg_path = top_path + "macro_placement.cfg"
if(os.path.exists(macro_placement_cfg_path)):
    rem = input('\nExisting macro_placement.cfg found on project path. Do you want to overwrite it? Type yes or no\n > ')
    if(rem == "yes"):
        os.remove(macro_placement_cfg_path)
    else:
        print("Aborting...")
        sys.exit()

# Read in config.tcl
with open(config_tcl_path, 'r', encoding="utf-8") as config_tcl:
    tconfig_tcl_data = config_tcl.read()

# Parse config.tcl and set various config variables


# config variables = Die area, macro areas, etc

# Create variable to hold the string that will eventually
# go into macro_placement.cfg

# Output to macro_placement.cfg