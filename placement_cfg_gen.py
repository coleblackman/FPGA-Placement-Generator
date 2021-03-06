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
dieX = input("\nPlease input desired die width (x-axis). Press enter for 2000.\n> ")
dieY = input("\nPlease input desired die height (y-axis). Press enter for 2200.\n> ")
gap = input("\nPlease input desired gap (the distance between two modules). Press enter for 100.\n>")
padding = input("\nPlease input desired padding (the distance between the edges and the outermost blocks). Press enter for 200.\n> ")
if dieX == "":
    dieX = "2000"
if dieY == "":
    dieY = "2200"
if gap == "":
    gap = "100"
if padding == "":
    padding = "200"

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
vertical_size = dieY

min_padding = padding

min_gap = int(gap)

blocks = foundMacros

block_width = macrox

block_height = macroy

# Generate the grid

###################################################

# Find smallest permissible gap between two centers
# This works because half_width*2 = block_width
min_width_dist = max(block_width)#+min_gap
print("HEREHEREHERHEREHEREHEREHRERE ", min_gap)
min_height_dist = max(block_height)#+min_gap 
min_dist = max(min_width_dist, min_height_dist)

# Calculate how many we can fit, 
# both horizontally and vertically
width_without_padding = (int(horizontal_size)-(int(min_padding)*2)) 
if width_without_padding < min_width_dist+min_gap+min_width_dist:
    print("Insufficient die width for more than a 1x1 grid.\nAborting...")
    sys.exit()
else: # now we know it is more than 1x1
    horizontal_number = 1 + (width_without_padding-min_width_dist)//(min_width_dist+min_gap)
    # add 1 for the last block, then divide by the blocks+ their respective gaps
print("horizontal_number ", horizontal_number)
print("horizontal_size ", horizontal_size)

height_without_padding = int(vertical_size)-(int(min_padding)*2)
if height_without_padding < min_height_dist+min_gap+min_height_dist:
    print("min_height_dist: ", min_height_dist)
    print("height without padding: ", height_without_padding)
    print("min_padding: ", min_padding)
    print("vertical size: ", vertical_size)
    print("Insufficient die height for more than a 1x1 grid.\nAborting...")
    sys.exit()
else:
    vertical_number = 1 + (height_without_padding-min_height_dist)//(min_height_dist+min_gap)
print("vertical_number:  ", vertical_number)

# TODO First create a 2d data structure that will hold what kind of macro to put at each point

macroTypeMatrix = [[0 for i in range(horizontal_number)] for j in range(vertical_number)]

# TODO Now populate it with just the grid_clbs:
for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        if i % 2 == 1 and j % 2 == 1: # found a grid_clb location
            macroTypeMatrix[i][j] = "grid_clb_"# + str(int(i/2)+1) + "_"
        elif i % 2 == 1 and j % 2 == 0: # found a cbx location
            macroTypeMatrix[i][j] = "cbx_" + "1" + "__" + str(int(j/2))+ "_"      
        elif i % 2 == 0 and j % 2 == 1: # found a cby location 
            macroTypeMatrix[i][j] = "cby_" + str(int(i/2)) + "__" + "1" + "_"
        elif i % 2 == 0 and j % 2 == 0: # found sb location (WORKING because sb's never have overlap)
            macroTypeMatrix[i][j] = "sb_" + str(int(i/2)) + "__" + str(int(j/2)) + "_"
print(macroTypeMatrix)

# Put all x and y coords for centers into lists

centers_x = [0 for i in range(horizontal_number)]
centers_y = [0 for i in range(vertical_number)]

# First define the bottom left block center coords:
index = macroNames.index(macroTypeMatrix[0][0])
prior_half = block_width[index]//2
centers_x[0] = int(min_padding) + prior_half
for i in range(horizontal_number):
    if i == 0:
        continue # iterate 4 times, from 1 to 4
    else:
        print("Analyzing i = ", i)
        index = macroNames.index(macroTypeMatrix[i-1][0])
        centers_x[i] = centers_x[i-1] + min_gap + prior_half + block_width[index]//2
        prior_half = centers_x[i-1]//2

index = macroNames.index(macroTypeMatrix[0][0])
prior_half = block_height[index]//2
centers_y[0] = int(min_padding) + prior_half    
for i in range(vertical_number):
    if i == 0:
        continue
    else:
        index = macroNames.index(macroTypeMatrix[0][i-1])
        centers_y[i] = centers_y[i-1] + min_gap + prior_half + block_height[index]//2
        prior_half = centers_y[i-1]//2

# macrox and macroy now contain the x and y coords of each block.
macrox = [[0 for i in range(horizontal_number)] for j in range(vertical_number)]
macroy = [[0 for i in range(horizontal_number)] for j in range(vertical_number)]
# TODO Assign to each module the correct coordinates from centers_y and centers_x


for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        macrox[i][j] = centers_x[i]

for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        macroy[i][j] = centers_y[i]



# Now define the variable that will be eventually written to macro_placement.cfg
macro_placement = ""

# Convert from centers to bottom-left corner
bottom_left_x = [[0 for i in range(horizontal_number)] for j in range(vertical_number)]
bottom_left_y = [[0 for i in range(horizontal_number)] for j in range(vertical_number)]
# Requires knowing what type each block is
# because the type determines the size
# use the variables macrox/macroy for coords and block_width and block_height for size

for i in range(len(macroTypeMatrix)):
    for j in range(len(macroTypeMatrix[i])):
        # Based on type of macro, get the x width
        # Find index 
        index = macroNames.index(macroTypeMatrix[i][j]) # Find what type of module we are placing
        bottom_left_x[i][j] = macrox[i][j] - block_width[index]//2
        print(bottom_left_y[i][j])
        print(macroy[j][i])
        print(block_height[index])
        bottom_left_y[i][j] = macroy[j][i] - block_height[index]//2 # problem is with macroy
        
        print("Placing at i = ", i, ". j = ", j, ". macrox[i][j] = ", macrox[i][j], ". macroy[i][j] = ", macroy[i][j], ". macroy[j][i] = ", macroy[j][i])
        # IMPORTANT lines, this assigns what will ultimately be written to the file
        if macroNames[index] == "grid_clb_":
            macro_placement += macroNames[index] + str(int(i/2)+1) + "__" + str(int(j/2)+1) + "_ " + str(bottom_left_x[i][j]) + " " + str(bottom_left_y[i][j]) + " N \n"
        elif macroNames[index][0:3] == "cbx":
            macro_placement += "cbx_" + str(int(i/2)+1) + "__" + str(int(j/2)) + "_ " + str(bottom_left_x[i][j]) + " " + str(bottom_left_y[i][j]) + " N \n"
        elif macroNames[index][0:3] == "cby":
            macro_placement += "cby_" + str(int(i/2)) + "__" + str(int(j/2)+1) + "_ " + str(bottom_left_x[i][j]) + " " + str(bottom_left_y[i][j]) + " N \n"
        else:
            macro_placement += macroNames[index] +  " " + str(bottom_left_x[i][j]) + " " + str(bottom_left_y[i][j]) + " N \n"


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


macro_placement_inst = ""
counter = 0


# Now add the inst_x lines if there are repeats
for i in range(len(macroNames)): # Iterate through every TYPE of macro
    if macro_placement.count(macroNames[i]) > 1: # If there is a macro that is used more than once
        for k in macro_placement.splitlines(): # Search every line for instances of that macro
            if k.count(macroNames[i]) > 0: # If the current line contains that macro
                #macro_placement_inst += k.replace(macroNames[i], (str(macroNames[i]) + str(counter+1))) + "\n"
                counter += 1
        counter = 0
        # Now that we have added replacements for all of the duplicate modules, remove their original copies
    for l in macro_placement.splitlines():
        if l.count(macroNames[i]) > 0 and macro_placement_inst.count(macroNames[i]) > 0:
            print("removing ", macroNames[i])
            macro_placement = macro_placement.replace(l, '')

macro_placement += macro_placement_inst
for u in macro_placement.splitlines():
    if u == "\n":
        macro_placement = macro_placement.replace(u, '')

macro_placement = "".join([s for s in macro_placement.splitlines(True) if s.strip("\r\n")])
#

#

# Write to the file
macro_file = open(macro_placement_path, "w")
macro_file.write(macro_placement)
print("\n\033[1;32mSuccessfully wrote to macro_placement.cfg\033[m\n")