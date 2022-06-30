# Ask for project directory
import sys
import os
import re

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

# Determine if there is a fpga_top, fpga_core, neither, or both
valid_fpga_top_found = False
valid_fpga_core_found = False

use_fpga_top = False
use_fpga_core = False

fpga_top_path = top_path + "fpga_top.v"
fpga_core_path = top_path + "fpga_core.v"

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

# Ensure there is a .gds for each macro

print("Searching for necessary macros in ", top_path, '/gds...')


# Source every single macro's config.tcl and get the sizes

# Read in overall config.tcl
with open(config_tcl_path, 'r', encoding="utf-8") as config_tcl:
    tconfig_tcl_data = config_tcl.read()

# Parse config.tcl and set various config variables
# Here is the regex: (?<=set \:\:env\(DIE_AREA\) ).*

Take a look here for inspiration https://stackoverflow.com/questions/4248010/how-to-exclude-comment-lines-when-searching-with-regular-expression

# config variables = Die area, macro areas, etc
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
horizontal_number = (horizontal_size-(min_padding*2))/(min_width_dist+min_gap)
vertical_number = (vertical_size-(min_padding*2))/(min_height_dist+min_gap)
# Put all x and y coords for centers into tuples

centers_x = [min_gap]
centers_y = [min_gap]

for i,x in enumerate(horizontal_number):
    centers_x.append(centers_x[i-1]+min_gap)

for i,y in enumerate(vertical_number):
    centers_y.append(centers_y[i-1]+min_gap)

# Convert from centers to bottom-left corner

# Requires knowing what type each block is
# because the type determines the size




# grid_clib = every other, except it can never be on an edge

# Output to macro_placement.cfg, neatly configured
# with the correct inst name from the gds file