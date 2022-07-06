rows = 3
cols = 2
a = []
for row in range(rows):
    a += [[0]*cols]


a[0][0] = "test2"
a[1][1] = "test"
print("   a =", a)