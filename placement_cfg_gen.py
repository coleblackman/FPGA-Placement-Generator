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

# Get desired die area
dieX = input("\nPlease input desired die width (x-axis). Press enter for 1610.\n> ")
dieY = input("\nPlease input desired die height (y-axis). Press enter for 1610.\n> ")
padding = input("\nPlease input desired padding. Press enter for 200.\n> ")
if dieX == "":
    dieX = 3000
if dieY == "":
    dieY = 3000
if padding == "":
    padding = 200

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

print("\nFound", numFoundMacros, "macro[s].\n")
print(foundMacros)

# Make a parallel array with just the paths of the macro modules
macroPaths = []
# Make a parallel array with just the names of the modules
macroNames = []
for macro in foundMacros:
    macroPaths.append((macro_tcl_path+"/"+macro))
    macroNames.append(macro[0:-10])

# Extract x and y sizes from each config.tcl
macrox = []
macroy = []
for i in range(len(macroNames)):
    with open(macroPaths[i], 'r', encoding="utf-8") as macro_tcl:
        macro_tcl_data = macro_tcl.read()
        search_term = re.compile("(?<=set \:\:env\(DIE_AREA\) ).*", re.MULTILINE|re.I)

        for match in search_term.finditer(macro_tcl_data): 
            found = match.group()
            macrox.append(int(found[5:-4]))
            macroy.append(int(found[9:12]))
            

horizontal_size = dieX
print("REF: horizontal Size: ", horizontal_size)
vertical_size = dieY
print("REF: vertical Size: ", vertical_size)

min_padding = padding
print("REF: minpadding: ", min_padding)

min_gap = 100
print("REF: min_gap: ", min_gap)

blocks = foundMacros
print("REF: blocks ", blocks)

block_width = macrox
print("REF block_width ", block_width)

block_height = macroy
print("REF: block_height ", block_height)


# Generate the grid

####################################################################################

# Find smallest permissible gap between two centers
# This works because half_width*2 = block_width
min_width_dist = max(block_width)+min_gap
min_height_dist = max(block_height)+min_gap
min_dist = max(min_width_dist, min_height_dist)

# Calculate how many we can fit, 
# both horizontally and vertically
horizontal_number = (horizontal_size-(min_padding*2))//(min_width_dist+min_gap)
vertical_number = (vertical_size-(min_padding*2))//(min_height_dist+min_gap)
print("vertical number: ", vertical_number)

# TODO First create a 2d data structure that will hold what kind of macro to put at each point
cols = horizontal_number
rows = vertical_number
macroTypeMatrix = [[0 for i in range(cols)] for j in range(rows)]

# TODO Now populate it with just the grid_clbs:
for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        if i % 2 == 1 and j % 2 == 1: # found a grid_clb location
            macroTypeMatrix[i][j] = "grid_clb_"
        elif i % 2 == 1 and j % 2 == 0: # found a cbx location
            macroTypeMatrix[i][j] = "cbx_" + "1" + "__" + str(int(j/2))+ "_"      
        elif i % 2 == 0 and j % 2 == 1: # found a cby location
            macroTypeMatrix[i][j] = "cby_" + str(int(i/2)) + "__" + "1" + "_"
        elif i % 2 == 0 and j % 2 == 0: # found sb location
            macroTypeMatrix[i][j] = "sb_" + str(int(i/2)) + "__" + str(int(j/2)) + "_"
print(macroTypeMatrix)

# Put all x and y coords for centers into lists

centers_x = [0 for i in range(horizontal_number)]
centers_y = [0 for i in range(vertical_number)]

# First define the bottom left block center coords:
index = macroNames.index(macroTypeMatrix[0][0])
prior_half = block_width[index]//2
centers_x[0] = min_padding + prior_half
for i in range(horizontal_number):
    if i == 0:
        continue
    else:
        index = macroNames.index(macroTypeMatrix[i][0])
        centers_x[i] = centers_x[i-1] + min_gap + prior_half + block_width[index]//2
        #print("REF: about to calculate centers_x[", i, "]. block_width[index] = ", block_width[index], "centers_x[i-1]: ", centers_x[i-1], "prior_half = ", prior_half, " min_gap = ", min_gap, ". centers_x[", i, "]= ", centers_x[i])
        prior_half = centers_x[i-1]//2

index = macroNames.index(macroTypeMatrix[0][0])
prior_half = block_height[index]//2
centers_y[0] = min_padding + prior_half    
for i in range(vertical_number):
    if i == 0:
        continue
    else:
        index = macroNames.index(macroTypeMatrix[0][i])
        centers_y[i] = centers_y[i-1] + min_gap + prior_half + block_height[index]//2
        prior_half = centers_y[i-1]//2

print("REF: centers_x: ", centers_x)
print("REF: centers_y: ", centers_y)



# macrox and macroy now contain the x and y coords of each block.
macrox = [[0 for i in range(cols)] for j in range(rows)]
macroy = [[0 for i in range(cols)] for j in range(rows)]
# TODO Assign to each module the correct coordinates from centers_y and centers_x

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("first print macrox size: ", len(macrox), "\n", macrox)
print("and centers_x: ", len(centers_x), centers_x)
print("cols: ", cols, " rows: ", rows)
for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        macrox[i][j] = centers_x[i]

for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        macroy[i][j] = centers_y[i]



# Now define the variable that will be eventually written to macro_placement.cfg
macro_placement = ""

# Convert from centers to bottom-left corner
bottom_left_x = [[0 for i in range(cols)] for j in range(rows)]
bottom_left_y = [[0 for i in range(cols)] for j in range(rows)]
# Requires knowing what type each block is
# because the type determines the size
# use the variables macrox/macroy for coords and block_width and block_height for size
print("00000000000000000000000000000000000\n000000000000000000000000000000\n")
print()
print("macroNames = ", macroNames)
print("\nmacrox = ", macrox)
print("\nmacroy = ", macroy)
for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        # Based on type of macro, get the x width
        # Find index 
        index = macroNames.index(macroTypeMatrix[i][j]) # Find what type of module we are placing
        bottom_left_x[i][j] = macrox[i][j] - block_width[index]//2
        bottom_left_y[i][j] = macroy[j][i] - block_height[index]//2
        
        print("Placing at i = ", i, ". j = ", j, ". macrox[i][j] = ", macrox[i][j], ". macroy[i][j] = ", macroy[i][j], ". macroy[j][i] = ", macroy[j][i])
        macro_placement += "\nPlace a " + macroNames[index] + " at " + str(bottom_left_x[i][j]) + ", " + str(bottom_left_y[i][j])



# Output to macro_placement.cfg, configured
# with the correct inst name from the gds file

macro_placement_path = top_path[0:-1] + "macro_placement.cfg"



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