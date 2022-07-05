# Ask for project directory
import math
import sys
import os
import re


if len(sys.argv) > 1:
    top_path = sys.argv[1]
    print("\n\033[1;32mProject\033[m location supplied as a script argument: \033[1;32m", top_path, "\033[m")
else:
    top_path = input('Input location of \033[1;32mproject\033[m, type \"local\" for local directory, or type \"default\" for default.\n> ')
    if top_path == "default" or top_path == "" or top_path == "local":
        top_path = '.'
# Set paths for config.tcl, macro_placement.cfg
config_tcl_path = top_path + "/config.tcl"
macro_placement_cfg_path = top_path + "macro_placement.cfg"
if(os.path.exists(macro_placement_cfg_path)):
    rem = input('\nExisting macro_placement.cfg found on project path. Do you want to overwrite it? Type yes or no\n > ')
    if(rem == "yes"):
        os.remove(macro_placement_cfg_path)
    else:
        print("Aborting...")
        sys.exit()

# Determine if there is a fpga_top, fpga_core, neither, or both
valid_fpga_top_found = False
valid_fpga_core_found = False

use_fpga_top = False
use_fpga_core = False

fpga_top_path = top_path + "/fpga_top.v"
fpga_core_path = top_path + "/fpga_core.v"

print("Searching for fpga_top.v at ", fpga_top_path)
print("Searching for fpga_core.v at ", fpga_core_path)

if(os.path.exists(fpga_top_path)):
    valid_fpga_top_found = True
if(os.path.exists(fpga_core_path)):
    valid_fpga_core_found = True

if valid_fpga_top_found and valid_fpga_core_found:
    print("Both an fpga_top.v and an fpga_core.v have been found.")
    top_core_input = input("Type \'core\' to use fpga_core.v or \'top\' to use fpga_top.v \n> ")
    if top_core_input == "core":
        use_fpga_core = True
    elif top_core_input == "top":
        use_fpga_top = True
elif valid_fpga_core_found:
    print("Valid fpga_core.v found.")
    use_fpga_core = True
elif valid_fpga_top_found:
    print("Valid fpga_top.v found.")
    use_fpga_top = True
else:
    print("No fpga_core.v or fpga_top.v found. Ensure one is available.\nAborting...")
    sys.exit()

# Use statistics about number of each module to calculate grid size
# TODO: reject comments

if(use_fpga_top):
    with open(fpga_top_path, 'r', encoding="utf-8") as fpga_top:
        fpga_top_data = fpga_top.read()
    numGridObjects = fpga_top_data.count("grid_clb")

elif(use_fpga_core):
    with open(fpga_core_path, 'r', encoding="utf-8") as fpga_core:
        fpga_core_data = fpga_core.read()
    numGridObjects = fpga_core_data.count("grid_clb")

grid_number = math.sqrt(numGridObjects)
print("grid_number: ", grid_number)

# TODO Ensure there is a .gds for each macro

print("Searching for necessary macros in ", top_path, '/gds...')
macro_tcl_path = top_path+"/macro_tcls"
foundMacros = os.walk(macro_tcl_path).__next__()[2]
numFoundMacros = len(foundMacros)

print("Found", numFoundMacros, "macro[s].")
print(foundMacros)

# Make a parallel array with just the paths of the macro modules
macroPaths = []
# Make a parallel array with just the names of the modules
macroNames = []
for macro in foundMacros:
    macroPaths.append((macro_tcl_path+"/"+macro))
    macroNames.append(macro[0:-4])
print(macroNames)
print(macroPaths)

    
# Ensure there is a valid overall config.tcl
print("Searching for valid config.tcl at ", config_tcl_path)
if(os.path.exists(config_tcl_path)):
    # Read in overall config.tcl
    print("Valid config.tcl found.")
    with open(config_tcl_path, 'r', encoding="utf-8") as config_tcl:
        config_tcl_data = config_tcl.read()
else:
    print("No valid config.tcl found. Ensure it is in the appropriate directory and is valid. \nAborting...")
    sys.exit()
    
# Parse config.tcl and set various config variables
# Here is the regex: (?<=set \:\:env\(DIE_AREA\) ).*
# Take a look here for inspiration https://stackoverflow.com/questions/4248010/how-to-exclude-comment-lines-when-searching-with-regular-expression
# FIXME does not return any output currently
ConfigTCLRegularExpression = re.compile("(?<=set \:\:env\(DIE_AREA\) ).*", re.MULTILINE|re.DOTALL)
for search in ConfigTCLRegularExpression.findall(config_tcl_data):
    print(search)
# config variables = Die area, macro areas, etc
# There are 4 types: grid_clb, sb_x_y, cbx_x_y, cby_x_y
# First, grid_clb:
grid_clb_path = top_path + "fpga_core/grid_clb/config.tcl"
# TODO Now read in that file and parse the width and height of the macro

horizontal_size = 6000

vertical_size = 6000
min_padding = 200
min_gap = 100
blocks = ("grid_clb", "cby", "sb")
block_width = (400, 200, 200)
block_height = (500, 200, 600)

# Create variable to hold the string that will eventually
# go into macro_placement.cfg
macro_placement = ""

# Generate the grid

# Find smallest permissible gap between two centers
# This works because half_width*2 = block_width
min_width_dist = max(block_width)+min_gap
min_height_dist = max(block_height)+min_gap
min_dist = max(min_width_dist, min_height_dist)

# Calculate how many we can fit, 
# both horizontally and vertically
print("\n---------------------------\n")
horizontal_number = (horizontal_size-(min_padding*2))//(min_width_dist+min_gap)
print("horizontal_number: ", horizontal_number)
vertical_number = (vertical_size-(min_padding*2))//(min_height_dist+min_gap)
print("vertical number: ", vertical_number)
# Put all x and y coords for centers into tuples

centers_x = [min_gap]
centers_y = [min_gap]

for i in range(horizontal_number-1):
    centers_x.append(centers_x[i-1]+min_gap)

for i in range(vertical_number-1):
    centers_y.append(centers_y[i-1]+min_gap)

# Convert from centers to bottom-left corner

# Requires knowing what type each block is
# because the type determines the size



# grid_clib = every other, except it can never be on an edge

# Output to macro_placement.cfg, configured
# with the correct inst name from the gds file

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