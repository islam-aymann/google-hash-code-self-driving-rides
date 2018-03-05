a = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2]

group = list()
whole = list()
start = a[0]
for ride in a:
    if ride == start:
        group.append(ride)
    else:
        whole.append(group)
        start = ride
        group = list()
        group.append(ride)
whole.append(group)

print(whole)