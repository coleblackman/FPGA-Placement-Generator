horizontal_size = 3000

vertical_size = 3000
min_padding = 200
min_gap = 100
blocks = ("grid_clb", "cby", "sb")
block_width = (400, 200, 200)
block_height = (500, 200, 600)

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
# Put all x and y coords for centers into tuples

centers_x = [min_gap]
centers_y = [min_gap]

for i in range(horizontal_number-1):
    centers_x.append(centers_x[i-1]+min_gap)

for i in range(vertical_number-1):
    centers_y.append(centers_y[i-1]+min_gap)

print("centers_x: ", centers_x)
print("centers_y: ", centers_y)

# Convert from centers to bottom-left corner

# Requires knowing what type each block is
# because the type determines the size



# Find if it is a grid_clb

# for i, x in enumerate()

# every other, except it can never be on an edge
