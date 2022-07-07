horizontal_size = 3000

vertical_size = 3000
min_padding = 200
min_gap = 100
blocks = ['sb_2__1_config.tcl', 'sb_1__1_config.tcl', 'cbx_1__0_config.tcl', 'grid_clb_config.tcl', 'sb_0__0_config.tcl', 'sb_2__2_config.tcl', 'cby_1__1_config.tcl', 'cby_2__1_config.tcl', 'cbx_1__2_config.tcl', 'sb_1__2_config.tcl', 'sb_0__2_config.tcl', 'cby_0__1_config.tcl', 'cbx_1__1_config.tcl', 'sb_1__0_config.tcl', 'sb_2__0_config.tcl', 'sb_0__1_config.tcl']
block_width = [200, 200, 200, 250, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
block_height = [210, 210, 210, 260, 210, 210, 210, 210, 210, 210, 210, 210, 210, 210, 210, 210]

# Find smallest permissible gap between two centers
# This works because half_width*2 = block_width
min_width_dist = max(block_width)+min_gap
min_height_dist = max(block_height)+min_gap
min_dist = max(min_width_dist, min_height_dist)

# Calculate how many we can fit,
# both horizontally and vertically
horizontal_number = (horizontal_size-(min_padding*2))//(min_width_dist+min_gap)
print("horizontal_number: ", horizontal_number)
vertical_number = (vertical_size-(min_padding*2))//(min_height_dist+min_gap)

print("vertical number: ", vertical_number)

# Put all x and y coords for centers into lists

centers_x = [0 for i in range(horizontal_number)]
centers_y = [0 for i in range(vertical_number)]

for i in range(horizontal_number-1):
    centers_x[i] = centers_x[i-1]+min_gap

for i in range(vertical_number-1):
    centers_y[i] = centers_y[i-1]+min_gap

print("centers_x: ", centers_x)
print("centers_y: ", centers_y)

# Convert from centers to bottom-left corner

# Requires knowing what type each block is
# because the type determines the size



# Find if it is a grid_clb

# for i, x in enumerate()

# every other, except it can never be on an edge
